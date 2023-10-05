import unittest

from sricheck.sricheck import SRICheck

class TestInit(unittest.TestCase):

    def test_init_with_url(self):
        check = SRICheck("https://www.4armed.com")
        self.assertEqual(check.url, "https://www.4armed.com")
    
    def test_init_without_args(self):
        with self.assertRaises(TypeError) as error:
            s = SRICheck()
        self.assertEquals(str(error.exception), "SRICheck.__init__() missing 1 required positional argument: 'url'")
    
    def test_init_with_empty_url(self):
        with self.assertRaises(ValueError) as error:
            s = SRICheck("")
        self.assertEquals(str(error.exception), "URL cannot be empty")
    
    def test_init_with_invalid_url(self):
        with self.assertRaises(ValueError) as error:
            s = SRICheck("ftp://www.4armed.com")
        self.assertEquals(str(error.exception), "URL must be http or https")