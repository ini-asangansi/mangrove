__author__ = 'jwishnie'

from unittest  import TestCase
from datetime import datetime
import utils

class TestUtils(TestCase):
    an_int = 1
    a_float = 2.1
    a_bool = True
    true_strings = ('y','Y','yes','yeS', 'yES', 'YES', 'Yes', '1', 't', 'T', 'True', 'TrUe')
    a_datetime = datetime.now()
    a_list = [1,2]
    a_tuple = (1,2)
    a_dict = {1:2}
    a_blank_string = ''
    a_ws_string = '          '
    a_string = 'abc'
    a_nonempty_ws_string = '      ab c  '
    an_empty_list = []
    an_empty_dict = {}
    an_empty_tupe = ()

    empties = (None, a_blank_string, a_ws_string, an_empty_dict, an_empty_list, an_empty_tupe)
    non_empties = (an_int, a_float, a_bool, a_datetime, a_list, a_tuple, a_dict, a_string, a_nonempty_ws_string)

    seqs = (a_list, a_tuple, a_dict, an_empty_dict, an_empty_list, an_empty_tupe, true_strings)
    non_seqs = (None, an_int, a_float, a_bool, a_string, a_blank_string, a_nonempty_ws_string)

    nums = (an_int, a_float, a_bool)
    non_nums = (None, a_list, a_tuple, a_dict, a_blank_string, a_nonempty_ws_string, a_string,
                an_empty_dict, an_empty_list, an_empty_tupe)

    def _test_a_list(self, pos, neg, test, pos_fail_msg, neg_fail_msg):
        for pos in pos:
            self.assertTrue(test(pos), "'%s' %s" % (str(pos), pos_fail_msg))

        for neg in neg:
            self.assertFalse(test(neg), "'%s' %s" % (str(neg), neg_fail_msg))
    
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
        self._test_a_list(self.nums,  self.non_nums, utils.is_number,
                          "failed 'is_number'", "passed 'is_number'")
