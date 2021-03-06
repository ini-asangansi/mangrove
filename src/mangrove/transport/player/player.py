# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
import csv
import re
import xlrd
from mangrove.errors.MangroveException import SMSParserInvalidFormatException, CSVParserInvalidHeaderFormatException, MangroveException, MultipleSubmissionsForSameCodeException, XlsParserInvalidHeaderFormatException
from mangrove.transport import reporter
from mangrove.transport.submissions import  SubmissionRequest
from mangrove.utils.types import is_empty, is_string


class Channel(object):
    SMS = "sms"
    WEB = "web"
    XFORMS = "xforms"
    CSV = "csv"
    XLS = "xls"


class Request(object):
    def __init__(self, transport, message, source, destination):
        self.transport = transport
        self.message = message
        self.source = source
        self.destination = destination


class Response(object):
    def __init__(self, reporters, submission_response):
        self.reporters = reporters if reporters is not None else []
        self.success = False
        self.errors = {}
        if submission_response is not None:
            self.success = submission_response.success
            self.submission_id = submission_response.submission_id
            self.errors = submission_response.errors
            self.datarecord_id = submission_response.datarecord_id
            self.short_code = submission_response.short_code
            self.processed_data = submission_response.processed_data


class SMSPlayer(object):
    def __init__(self, dbm, submission_handler):
        self.dbm = dbm
        self.submission_handler = submission_handler

    def accept(self, request):
        assert request is not None
        assert request.source is not None
        assert request.destination is not None
        assert request.message is not None
        reporters = reporter.find_reporter(self.dbm, request.source)
        sms_parser = SMSParser()
        form_code, values = sms_parser.parse(request.message)
        submission_request = SubmissionRequest(form_code=form_code, submission=values, transport=request.transport,
                                               source=request.source, destination=request.destination)
        submission_response = self.submission_handler.accept(submission_request)
        return Response(reporters=reporters, submission_response=submission_response)


class SMSParser(object):
    MESSAGE_PREFIX = ur'^(\w+)\s+\+(\w+)\s+(\w+)'
    MESSAGE_TOKEN = ur"(\S+)(.*)"
    SEPARATOR = u"+"

    def __init__(self):
        pass

    def _to_unicode(self, message):
        if type(message) is not unicode:
            message = unicode(message, encoding='utf-8')
        return message

    def _clean(self, message):
        message = self._to_unicode(message)
        return message.strip()

    def _pop_form_code(self, tokens):
        form_code = tokens[0].strip().lower()
        tokens.remove(tokens[0])
        return form_code

    def _parse_tokens(self, tokens):
        tokens = [token.strip() for token in tokens if token]
        submission = {}
        for token in tokens:
            if is_empty(token): continue
            field_code, answer = self._parse_token(token)
            if field_code in submission.keys():
                raise MultipleSubmissionsForSameCodeException(field_code)
            submission[field_code] = answer
        return submission

    def _parse_token(self, token):
        m = re.match(self.MESSAGE_TOKEN, token, flags=re.UNICODE)  # Match first non white space set of values.
        field_code, value = m.groups()
        return field_code.lower(), value.strip()

    def _validate_format(self, message):
        if not re.match(self.MESSAGE_PREFIX, message, flags=re.UNICODE):
            raise SMSParserInvalidFormatException(message)
    
    def parse(self, message):
        assert is_string(message)
        message = self._clean(message)
        self._validate_format(message)
        tokens = message.split(self.SEPARATOR)
        form_code = self._pop_form_code(tokens)
        submission = self._parse_tokens(tokens)
        return form_code, submission



class WebPlayer(object):
    def __init__(self, dbm, submission_handler):
        self.dbm = dbm
        self.submission_handler = submission_handler

    def accept(self, request):
        assert request is not None
        assert request.source is not None
        assert request.destination is not None
        assert request.message is not None
        web_parser = WebParser()
        form_code, values = web_parser.parse(request.message)
        submission_request = SubmissionRequest(form_code=form_code, submission=values, transport=request.transport,
                                               source=request.source, destination=request.destination)
        submission_response = self.submission_handler.accept(submission_request)
        return Response(reporters=[], submission_response=submission_response)


class WebParser(object):
    def parse(self, message):
        form_code = message.pop('form_code')
        return form_code, message


class CsvPlayer(object):
    def __init__(self, dbm, submission_handler, parser):
        self.dbm = dbm
        self.submission_handler = submission_handler
        self.parser = parser

    def accept(self, csv_data):
        responses = []
        submissions = self.parser.parse(csv_data)
        for (form_code, values) in submissions:
            submission_request = SubmissionRequest(form_code=form_code, submission=values, transport=Channel.CSV,
                                                   source=Channel.CSV, destination="")
            try:
                submission_response = self.submission_handler.accept(submission_request)
                response= Response(reporters=[],submission_response=submission_response)
                if not submission_response.success:
                    response.errors = dict(error=submission_response.errors.values(), row=values)
                responses.append(response)
            except MangroveException as e:
                response = Response(reporters=[], submission_response=None)
                response.success=False
                response.errors = dict(error=e.message, row=values)
                responses.append(response)
        return responses


class CsvParser(object):
    def _next_line(self, dict_reader):
        return dict_reader.next().values()[0]

    def _parse_header(self, dict_reader):
        field_header = dict_reader.fieldnames
        while is_empty(field_header) or self._has_empty_values(field_header):
            try:
                field_header = self._next_line(dict_reader)
            except StopIteration:
                raise CSVParserInvalidHeaderFormatException()
        return [field.strip().lower() for field in field_header]

    def _strip_field_values(self, row):
        for key, value in row.items():
            if value is not None and is_string(value):
                row[unicode(key, encoding='utf-8')] = unicode(value.strip(), encoding='utf-8')

    def _parse_row(self, form_code_fieldname, row):
        result_row = dict(row)
        self._strip_field_values(result_row)
        form_code = result_row.pop(form_code_fieldname).lower()
        return form_code, result_row

    def parse(self, csv_data):
        assert not is_string(csv_data)
        dict_reader = csv.DictReader(csv_data, restkey='extra_values')
        dict_reader.fieldnames = self._parse_header(dict_reader)
        parsedData = []
        form_code_fieldname = dict_reader.fieldnames[0]
        for row in dict_reader:
            parsedData.append(self._parse_row(form_code_fieldname, row))
        return parsedData

    def _has_empty_values(self, values_list):
        for value in values_list:
            if is_empty(value):
                return True
        return False


class XlsPlayer(object):
    def __init__(self, dbm, submission_handler, parser):
        self.dbm = dbm
        self.submission_handler = submission_handler
        self.parser = parser

    def accept(self, file_contents):
        responses = []
        submissions = self.parser.parse(file_contents)
        for (form_code, values) in submissions:
            submission_request = SubmissionRequest(form_code=form_code, submission=values, transport=Channel.XLS,
                                                   source=Channel.XLS, destination="")
            try:
                submission_response = self.submission_handler.accept(submission_request)
                response= Response(reporters=[],submission_response=submission_response)
                if not submission_response.success:
                    response.errors = dict(error=submission_response.errors.values(), row=values)
                responses.append(response)
            except MangroveException as e:
                response = Response(reporters=[], submission_response=None)
                response.success=False
                response.errors = dict(error=e.message, row=values)
                responses.append(response)
        return responses


class XlsParser(object):
    def parse(self, xls_contents):
        assert xls_contents is not None
        workbook = xlrd.open_workbook(file_contents=xls_contents)
        worksheet = workbook.sheets()[0]
        header_found = False
        header = None
        parsedData = []
        for row_num in range(worksheet.nrows):
            row = worksheet.row_values(row_num)

            if not header_found:
                header, header_found = self._is_header_row(row)
                continue
            if self._is_empty(row):
                continue

            row = self._clean(row)
            row_dict = dict(zip(header, row))
            form_code, values = (row_dict.pop(header[0]).lower(), row_dict)
            parsedData.append((form_code, values))
        if not header_found:
            raise XlsParserInvalidHeaderFormatException()
        return parsedData


    def _is_header_row(self, row):
        if is_empty(row[0]):
            return None, False
        return [str(value).strip().lower() for value in row], True

    def _clean(self, row):
        return [str(value).strip() for value in row]

    def _is_empty(self, row):
        return len([value for value in row if not is_empty(value)]) == 0



        