# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
import os
import unittest
from mock import Mock
from mangrove.datastore.database import DatabaseManager
from mangrove.errors.MangroveException import FormModelDoesNotExistsException
from mangrove.transport.player.player import XlsPlayer, XlsParser
from mangrove.transport.submissions import SubmissionHandler, SubmissionResponse
import xlwt

class TestXlsPlayer(unittest.TestCase):
    def setUp(self):
        self.dbm = Mock(spec=DatabaseManager)
        self.submission_handler_mock = Mock(spec=SubmissionHandler)
        self.parser = XlsParser()
        self.csv_data = """
                                FORM_CODE,ID,BEDS,DIRECTOR,MEDS
                                CLF1,CL001,10,Dr. A,201
                                CLF1,CL002,11,Dr. B,202

                                CLF2,CL003,12,Dr. C,203
                                CLF1,CL004,13,Dr. D,204
                                
                                CLF1,CL005,14,Dr. E,205
"""
        self.file_name = 'test.xls'
        wb = xlwt.Workbook()
        ws = wb.add_sheet('test')
        for row_number, row  in enumerate(self.csv_data.split('\n')):
            for col_number, val in enumerate(row.split(',')):
                ws.write(row_number, col_number, val)
        wb.save(self.file_name)
        self.player = XlsPlayer(self.dbm, self.submission_handler_mock, self.parser)

    def test_should_import_xls_string(self):
        self.player.accept(file_contents=open(self.file_name).read())
        self.assertEqual(5, self.submission_handler_mock.accept.call_count)

    def test_should_process_next_submission_if_exception_with_prev(self):
        def expected_side_effect(*args, **kwargs):
            request = kwargs.get('request') or args[0]
            if request.form_code == 'clf2':
                raise FormModelDoesNotExistsException('')
            return SubmissionResponse(success=True, submission_id=1)

        self.submission_handler_mock.accept.side_effect = expected_side_effect

        response = self.player.accept(file_contents=open(self.file_name).read())
        self.assertEqual(5, len(response))
        self.assertEqual(False, response[2].success)

        success = len([index for index in response if index.success])
        total = len(response)
        self.assertEqual(4, success)
        self.assertEqual(5, total)

    def tearDown(self):
        os.remove(self.file_name)
