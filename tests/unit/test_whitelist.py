import unittest

from sricheck.sricheck import SRICheck

class TestWhitelisting(unittest.TestCase):

    def test_google_fonts_is_whitelisted(self):
        check = SRICheck("https://www.4armed.com")
        self.assertEqual(check.is_whitelisted("fonts.googleapis.com"), True)
    
    def test_google_tag_manager_is_whitelisted(self):
        check = SRICheck("https://www.4armed.com")
        self.assertEqual(check.is_whitelisted("www.googletagmanager.com"), True)
    
    def test_hubspot_is_whitelisted(self):
        check = SRICheck("https://www.4armed.com")
        self.assertEqual(check.is_whitelisted("js.hs-scripts.com"), True)
    
    def test_target_url_is_whitelisted(self):
        check = SRICheck("https://www.4armed.com")
        self.assertEqual(check.is_whitelisted("www.4armed.com"), True)
    
    def test_additional_ignored_host_is_whitelisted(self):
        check = SRICheck("https://www.4armed.com")
        check.add_whitelisted_host("cdn.4armed.com")
        self.assertEqual(check.is_whitelisted("cdn.4armed.com"), True)
    
    def test_unknown_host_is_not_whitelisted(self):
        check = SRICheck("https://www.4armed.com")
        self.assertEqual(check.is_whitelisted("www.google.com"), False)
    
    def test_unknown_host_is_not_whitelisted_when_additional_ignored_hosts_are_set(self):
        check = SRICheck("https://www.4armed.com")
        check.add_whitelisted_host("cdn.4armed.com")
        self.assertEqual(check.is_whitelisted("www.google.com"), False)
    
    def test_regex_pattern_is_whitelisted(self):
        check = SRICheck("https://www.4armed.com")
        check.add_whitelisted_host(".*\.4armed\.com")
        self.assertEqual(check.is_whitelisted("cdn.4armed.com"), True)

if __name__ == '__main__':
    unittest.main()