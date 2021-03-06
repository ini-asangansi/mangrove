# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from unittest import TestCase
import os
from mangrove.errors.MangroveException import SMSParserInvalidFormatException, CSVParserInvalidHeaderFormatException, XlsParserInvalidHeaderFormatException
from mangrove.transport.player.player import SMSParser, WebParser, CsvParser, XlsParser
import xlwt


class TestSMSParser(TestCase):
    def test_should_return_all_field_codes_in_lower_case(self):
        smsplayer = SMSParser()
        form_code, values = smsplayer.parse("WP +id 1 +Name FirstName +aGe 10")
        self.assertEqual({"id": "1", "name": "FirstName", "age": "10"}, values)

    def test_should_preserve_non_leading_white_spaces_in_answer(self):
        smsplayer = SMSParser()
        form_code, values = smsplayer.parse("WP +ID 1 +NAME FirstName LastName +AGE 10")
        self.assertEqual({"id": "1", "name": "FirstName LastName", "age": "10"}, values)

    def test_should_parse_incomplete_messages_with_no_answer_values(self):
        smsplayer = SMSParser()
        form_code, values = smsplayer.parse("WP +ID 1 +BC ")
        self.assertEqual({"id": "1", "bc": ""}, values)

    def test_should_raise_error_if_invalid_sms_format(self):
        smsplayer = SMSParser()
        with self.assertRaises(SMSParserInvalidFormatException):
            form_code, values = smsplayer.parse("+")

        with self.assertRaises(SMSParserInvalidFormatException):
            form_code, values = smsplayer.parse("  +  ")

        with self.assertRaises(SMSParserInvalidFormatException):
            form_code, values = smsplayer.parse("  +  +")

        with self.assertRaises(SMSParserInvalidFormatException):
            form_code, values = smsplayer.parse("+WP ")

        with self.assertRaises(SMSParserInvalidFormatException):
            form_code, values = smsplayer.parse("WP")

        with self.assertRaises(SMSParserInvalidFormatException):
            form_code, values = smsplayer.parse("WP+")

        with self.assertRaises(SMSParserInvalidFormatException):
            form_code, values = smsplayer.parse(" WP ")

        with self.assertRaises(SMSParserInvalidFormatException):
            form_code, values = smsplayer.parse("WP ID")

        with self.assertRaises(SMSParserInvalidFormatException):
            form_code, values = smsplayer.parse("WP +ID")

    def test_should_accept_only_strings(self):
        sms_parser = SMSParser()
        with self.assertRaises(AssertionError):
            sms_parser.parse(10)
        with self.assertRaises(AssertionError):
            sms_parser.parse(None)



    def test_should_accept_unicode(self):
        sms_parser = SMSParser()
        form_code, values = sms_parser.parse(u"reg +s Āgra +n شصلكقم +m 080 +t clinic")
        self.assertEqual({u"s": u"Āgra", u"n": u"شصلكقم", u"m": u"080", u"t": u"clinic"}, values)


    def test_should_convert_input_to_unicode(self):
        sms_parser = SMSParser()
        form_code, values = sms_parser.parse("reg +s Āgra +n شصلكقم +m 080 +t clinic")
        self.assertEqual({u"s": u"Āgra", u"n": u"شصلكقم", u"m": u"080", u"t": u"clinic"}, values)


    def test_should_ignore_additional_separators(self):
        smsplayer = SMSParser()
        form_code, values = smsplayer.parse("WP +ID 1 + ++ +NAME FirstName LastName ++ +AGE 10 ++ ")
        self.assertEqual({"id": "1", "name": "FirstName LastName", "age": "10"}, values)
        self.assertEqual("wp", form_code)


    def test_should_return_form_code_and_message_as_dict(self):
        player = WebParser()
        message = {'form_code': 'X1', 'q1': 'a1', 'q2': 'a2'}
        form_code, values = player.parse(message)
        self.assertEquals(form_code, 'X1')
        self.assertEquals(values, {'q1': 'a1', 'q2': 'a2'})


class TestCsvParser(TestCase):
    def test_should_parse_csv_string(self):
        csv_data = """FORM_CODE,ID,BEDS,DIRECTOR,MEDS
        CLF1, CL001, 11, Dr. A1,201
        CLF1,CL002,12,Dr. A2,202
        CLF1,CL003,13,Dr. A3,203
        CLF1,CL004,14,Dr. A4,204
        CLF1,CL005,15,Dr. A5,205"""

        csv_parser = CsvParser()
        results = csv_parser.parse(csv_data.split("\n"))

        self.assertEqual(5, len(results))

        for index, result in enumerate(results):
            form_code, values = results[index]
            self.assertEqual("clf1", form_code)
            offset = index + 1
            self.assertEqual(
                    {"id": "CL%03d" % (offset,), "beds": "%d" % (10 + offset,),
                     "director": "Dr. A%d" % (offset,),
                     "meds": "%d" % (200 + offset,)
                }, values)

    def test_should_parse_csv_string_with_partial_values(self):
        csv_data = """FORM_CODE,ID,BEDS,DIRECTOR,MEDS
        CLF1, CL001, 11, Dr. A1,201

        CLF1, CL001,, Dr. A1,201

        CLF1,CL002,12,"Dr. LastName,Firstname" """

        csv_parser = CsvParser()
        results = csv_parser.parse(csv_data.split("\n"))

        self.assertEqual(3, len(results))

        form_code, values = results[0]
        self.assertEqual("clf1", form_code)
        self.assertEqual(
                {"id": "CL001", "beds": "11",
                 "director": "Dr. A1",
                 "meds": "201"
            }, values)
        form_code, values = results[1]
        self.assertEqual("clf1", form_code)
        self.assertEqual(
                {"id": "CL001", "beds": "",
                 "director": "Dr. A1",
                 "meds": "201"
            }, values)

        form_code, values = results[2]
        self.assertEqual("clf1", form_code)
        self.assertEqual(
                {"id": "CL002", "beds": "12",
                 "director": "Dr. LastName,Firstname",
                 "meds": None
            }, values)

    def test_should_parse_csv_string_with_empty_lines(self):
        csv_data = """
        

        FORM_CODE,ID,BEDS,DIRECTOR,MEDS

        CLF1, CL001, 11, Dr. A1,201
        CLF1,CL002,12,Dr. A2,202

        CLF1,CL003,13,Dr. A3,203

        CLF1,CL004,14,Dr. A4,204
        CLF1,CL005,15,Dr. A5,205

"""

        csv_parser = CsvParser()
        results = csv_parser.parse(csv_data.split("\n"))

        self.assertEqual(5, len(results))

        for index, result in enumerate(results):
            form_code, values = results[index]
            self.assertEqual("clf1", form_code)
            offset = index + 1
            self.assertEqual(
                    {"id": "CL%03d" % (offset,), "beds": "%d" % (10 + offset,),
                     "director": "Dr. A%d" % (offset,),
                     "meds": "%d" % (200 + offset,)
                }, values)

    def test_should_raise_exception_for_invalid_format(self):
        empty_csv_data = """


     """

        csv_parser = CsvParser()
        with self.assertRaises(CSVParserInvalidHeaderFormatException):
            results = csv_parser.parse(empty_csv_data.split("\n"))


class TestXlsParser(TestCase):
    def setUp(self):
        data = """
                                FORM_CODE,ID,BEDS,DIRECTOR,MEDS

                                CLF1,CL001,10,Dr. A,201
                                CLF1,CL002,11,Dr. B,202
                                
                                CLF2,CL003,12,Dr. C,203
                                CLF1,CL004,13,Dr. D,204
                                CLF1,CL005,14,Dr. E,205
                                
"""
        self.file_name = "test.xls"
        wb = xlwt.Workbook()
        ws = wb.add_sheet('test')
        for row_number, row  in enumerate(data.split('\n')):
            for col_number, val in enumerate(row.split(',')):
                ws.write(row_number, col_number, val)
        wb.save(self.file_name)
        self.parser = XlsParser()

    def test_should_parse_xls_contents(self):
        input_file = open(self.file_name)
        submissions = self.parser.parse(input_file.read())
        self.assertEqual(5, len(submissions))
        form_code, values = submissions[0]
        self.assertEqual("clf1", form_code)
        self.assertEqual({"id": 'CL001', 'beds': '10', 'director': 'Dr. A', 'meds': '201'}, values)
        input_file.close()

    def test_should_raise_exception_for_invalid_format(self):
        data = """




"""
        os.remove(self.file_name)
        self.file_name = "test.xls"
        wb = xlwt.Workbook()
        ws = wb.add_sheet('test')
        for row_number, row  in enumerate(data.split('\n')):
            for col_number, val in enumerate(row.split(',')):
                ws.write(row_number, col_number, val)
        wb.save(self.file_name)
        input_file = open(self.file_name)
        with self.assertRaises(XlsParserInvalidHeaderFormatException):
            self.parser.parse(input_file.read())
        input_file.close()


    def tearDown(self):
        os.remove(self.file_name)
