# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
import unittest
from datawinners.messageprovider.messages import success_messages, REGISTRATION, SUBMISSION
from mangrove.errors.MangroveException import FormModelDoesNotExistsException, NumberNotRegisteredException,\
    MangroveException, EntityQuestionCodeNotSubmitted
from datawinners.messageprovider.message_handler import get_exception_message_for, get_submission_error_message_for, get_success_msg_for_submission_using, get_success_msg_for_registration_using
from mangrove.transport.player.player import Response


class TestGetExceptionMessageHandler(unittest.TestCase):
    def test_should_return_message_for_exception_for_channel(self):
        message = get_exception_message_for(exception=FormModelDoesNotExistsException("QC1"), channel="sms")
        expected_message = "Error with Questionnaire ID QC1. Find the Questionnaire ID on the printed questionnaire and resend SMS"
        self.assertEqual(expected_message, message)


    def test_should_return_default_message_for_exception_for_no_channel_passed(self):
        message = get_exception_message_for(exception=FormModelDoesNotExistsException("QC1"))
        expected_message = "Questionnaire ID QC1 doesnt exist."
        self.assertEqual(expected_message, message)


    def test_should_return_default_msg_for_exception_if_channel_specific_msg_missing(self):
        message = get_exception_message_for(exception=NumberNotRegisteredException("1234567890"), channel="web")
        expected_message = "This telephone number is not registered in our system."
        self.assertEqual(expected_message, message)


    def test_should_return_default_exception_message_for_unknown_exception(self):
        message = get_exception_message_for(exception=MangroveException(message="This is an error"), channel="web")
        expected_message = "This is an error"
        self.assertEqual(expected_message, message)

    def test_should_return_valid_message_even_if_code_is_None(self):
        message = get_exception_message_for(exception=EntityQuestionCodeNotSubmitted(), channel="web")
        expected_message = "You have not created a question asking the collector for the subject he is reporting on"
        self.assertEqual(expected_message, message)

    def test_should_return_valid_message_if_its_not_parameterized(self):
        message = get_exception_message_for(exception=NumberNotRegisteredException("1234567"), channel="web")
        expected_message = "This telephone number is not registered in our system."
        self.assertEqual(expected_message, message)


class TestShouldTemplatizeMessage(unittest.TestCase):
    def test_should_format_error_message_with_question_codes(self):
        expected_message = "Error. Invalid Submission. Refer to printed Questionnaire. Resend the question ID and answer for q1, q2"
        errors = {"q1": "Some error", "q2": "Some other error"}
        message = get_submission_error_message_for(errors)
        self.assertEqual(expected_message, message)

    def test_should_format_success_message_for_submission_with_reporter_name(self):
        expected_message = success_messages[SUBMISSION] % "rep1" + "age: 12 name: tester choice: red"
        response = Response(reporters=[{"name": "rep1"}], success=True, errors={}, processed_data={'name':'tester','age':12,'choice':['red']})
        message = get_success_msg_for_submission_using(response)
        self.assertEqual(expected_message, message)

    def test_should_format_success_message_for_submission_with_blank_if_no_reporter(self):
        expected_message = success_messages[SUBMISSION] % "" + "name: tester"
        response = Response(reporters=[], success=True, errors={}, processed_data={"name":"tester"})
        message = get_success_msg_for_submission_using(response)
        self.assertEqual(expected_message, message)

    def test_should_format_success_message_for_registration_with_short_code(self):
        expected_message = success_messages[REGISTRATION] % "Reporter identification number: REP1"
        response = Response(reporters=[], success=True, errors={}, short_code="REP1")
        message = get_success_msg_for_registration_using(response, "Reporter", "web")
        self.assertEqual(expected_message, message)
