import unittest

from sricheck.sricheck import SRICheck

class TestHeaders(unittest.TestCase):
    def test_with_standard_headers(self):
        check = SRICheck("https://www.4armed.com")
        self.assertEqual(check.headers["User-Agent"], "4ARMED SRI Check (https://github.com/4armed/sri-check)")