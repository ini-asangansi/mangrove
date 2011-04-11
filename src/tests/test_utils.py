# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

__author__ = 'jwishnie'

from unittest  import TestCase
from datetime import datetime
import utils

class TestUtils(TestCase):
    an_int = 1
    a_float = 2.1
    a_bool = True
    true_strings = ('y','Y','yes','yeS', 'yES', 'YES', 'Yes', '1', 't', 'T', 'True', 'TrUe',
                    u'y', u'Y', u'yes', u'yeS', u'yES', u'YES', u'Yes', u'1', u't', u'T', u'True', u'TrUe',
                    )
    not_true_strings = ('a',u"v", 0, None, ())
    a_datetime = datetime.now()
    a_list = [1,2]
    a_tuple = (1,2)
    a_dict = {1:2}
    a_blank_string = ''
    a_blank_unicode = u''
    a_ws_string = '          '
    a_ws_unicode = u'       '
    a_string = 'abc'
    a_unicode = u'你好吗？'
    a_nonempty_ws_unicode = u'      你好吗？    '
    a_nonempty_ws_string = '      ab c  '
    an_empty_list = []
    an_empty_dict = {}
    an_empty_tupe = ()

    empties = (
                None, a_blank_string, a_ws_string, an_empty_dict,
                an_empty_list, an_empty_tupe, a_blank_unicode, a_ws_unicode
    )

    non_empties = (
                    an_int, a_float, a_bool, a_datetime, a_list, a_tuple, a_dict,
                    a_string, a_nonempty_ws_string, a_unicode, a_nonempty_ws_unicode
    )

    seqs = (a_list, a_tuple, a_dict, an_empty_dict, an_empty_list, an_empty_tupe, true_strings)
    non_seqs = (
                None, an_int, a_float, a_bool, a_string, a_blank_string, a_nonempty_ws_string,
                a_unicode, a_blank_unicode, a_ws_unicode, a_nonempty_ws_unicode
    )

    nums = (an_int, a_float)
    non_nums = (None, a_list, a_tuple, a_dict, a_blank_string, a_nonempty_ws_string, a_string, an_empty_dict,
                an_empty_list, an_empty_tupe, a_unicode, a_blank_unicode, a_ws_unicode, a_nonempty_ws_unicode
    )

    strs = (
            a_string, a_unicode, a_ws_string, a_ws_unicode,
            a_nonempty_ws_unicode, a_nonempty_ws_string, a_blank_unicode, a_blank_string
    )
    
    non_strs = (
                None, an_int, a_float, a_bool, a_datetime, a_list, a_tuple, a_dict, an_empty_dict,
                an_empty_list, an_empty_tupe
    )

    bools = (True, False)
    non_bools = (
                 None, a_blank_string, a_ws_string, an_empty_dict,
                 an_empty_list, an_empty_tupe, a_blank_unicode, a_ws_unicode,
                 an_int, a_float, a_datetime, a_list, a_tuple, a_dict,
                 a_string, a_nonempty_ws_string, a_unicode, a_nonempty_ws_unicode
    )

    def _test_a_list(self, pos, neg, test, pos_fail_msg, neg_fail_msg):
        if pos is not None:
            for pos in pos:
                self.assertTrue(test(pos), "'%s' %s" % (unicode(pos), pos_fail_msg))

        if neg is not None:
            for neg in neg:
                self.assertFalse(test(neg), "'%s' %s" % (unicode(neg), neg_fail_msg))
    
    def test_empty(self):
        self._test_a_list(self.empties, self.non_empties, utils.is_empty,
                         "failed 'is_empty'", "passed 'is_empty'")

    def test_not_empty(self):
        self._test_a_list(self.non_empties, self.empties, utils.is_not_empty,
                         "failed 'is_not_empty'", "passed 'is_not_empty'")

    def test_is_sequence(self):
        self._test_a_list(self.seqs, self.non_seqs, utils.is_sequence,
                          "failed 'is_sequence'", "passed 'is_sequence'")

    def test_is_number(self):
        self._test_a_list([True, False]+list(self.nums),  self.non_nums, utils.is_number,
                          "failed 'is_number'", "passed 'is_number'")

    def test_is_string(self):
        self._test_a_list(self.strs,  self.non_strs, utils.is_string,
                          "failed 'is_string'", "passed 'is_string'")

    def test_string_as_bool(self):
        self._test_a_list(self.true_strings, self.not_true_strings,
                          lambda x : utils.string_as_bool(x),
                          ": string_as_bool returned 'False'", ": string_as_bool returned 'True'")

    def test_primitive_type(self):
        self._test_a_list(self.strs, None,
                          lambda x : utils.primitive_type(x) == 'text',
                          ": primitive_type returned something other than 'text'", "")

        self._test_a_list(self.nums, None,
                          lambda x : utils.primitive_type(x) == 'numeric',
                          ": primitive_type returned something other than 'numeric'", "")

        self._test_a_list([self.a_datetime], None,
                          lambda x : utils.primitive_type(x) == 'datetime',
                          ": primitive_type returned something other than 'datetime'", "")

        self._test_a_list(self.bools, None,
                          lambda x : utils.primitive_type(x) == 'boolean',
                          ": primitive_type returned something other than 'boolean'", "")

        self._test_a_list([None], None,
                          lambda x : utils.primitive_type(x) == 'unknown',
                          ": primitive_type returned something other than 'unknown'", "")

        
    def test_should_raise_ValueError_if_invalid_date_string(self):
        self.assertRaises(ValueError,utils.string_from_couch_to_date,"invalid date")
        self.assertRaises(ValueError,utils.string_from_couch_to_date,"")
        self.assertRaises(ValueError,utils.string_from_couch_to_date," ")

