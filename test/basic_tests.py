from unittest import TestCase

class SimpleTest(TestCase):
    def test_something(self):
        pass
    
    def test_failure_on_hudson(self):
        self.assertTrue(False)