import unittest

from sricheck.sricheck import SRICheck

class Testallowlisting(unittest.TestCase):

    def test_google_fonts_is_allowlisted(self):
        check = SRICheck("https://www.4armed.com")
        self.assertEqual(check.is_allowlisted("fonts.googleapis.com"), True)
    
    def test_google_tag_manager_is_allowlisted(self):
        check = SRICheck("https://www.4armed.com")
        self.assertEqual(check.is_allowlisted("www.googletagmanager.com"), True)
    
    def test_hubspot_is_allowlisted(self):
        check = SRICheck("https://www.4armed.com")
        self.assertEqual(check.is_allowlisted("js.hs-scripts.com"), True)
    
    def test_google_fonts_is_not_allowlisted_when_skip_checks_is_true(self):
        check = SRICheck("https://www.4armed.com")
        check.set_skip_checks(True)
        self.assertEqual(check.is_allowlisted("fonts.googleapis.com"), False)
    
    def test_target_url_is_allowlisted(self):
        check = SRICheck("https://www.4armed.com")
        self.assertEqual(check.is_allowlisted("www.4armed.com"), True)
    
    def test_additional_ignored_host_is_allowlisted(self):
        check = SRICheck("https://www.4armed.com")
        check.add_allowlisted_host("cdn.4armed.com")
        self.assertEqual(check.is_allowlisted("cdn.4armed.com"), True)
    
    def test_unknown_host_is_not_allowlisted(self):
        check = SRICheck("https://www.4armed.com")
        self.assertEqual(check.is_allowlisted("www.google.com"), False)
    
    def test_unknown_host_is_not_allowlisted_when_additional_ignored_hosts_are_set(self):
        check = SRICheck("https://www.4armed.com")
        check.add_allowlisted_host("cdn.4armed.com")
        self.assertEqual(check.is_allowlisted("www.google.com"), False)
    
    def test_regex_pattern_is_allowlisted(self):
        check = SRICheck("https://www.4armed.com")
        check.add_allowlisted_host(".*\.4armed\.com")
        self.assertEqual(check.is_allowlisted("cdn.4armed.com"), True)

if __name__ == '__main__':
    unittest.main()