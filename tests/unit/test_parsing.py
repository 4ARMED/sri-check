import unittest

from sricheck.sricheck import SRICheck

class TestParsing(unittest.TestCase):

    def test_script_tag_on_third_party_with_no_sri_returns_result(self):
        check = SRICheck("https://www.4armed.com")
        html = """<html><head><script src="https://cdn.cloudflare.com/script.js"></script></head></html>"""
        remote_resource_tags = check.get_remote_resource_tags(html)
        self.assertEqual(len(remote_resource_tags), 1)
        self.assertEqual(remote_resource_tags[0]['tag']['src'], "https://cdn.cloudflare.com/script.js")
    
    def test_script_tag_on_own_host_with_no_sri_returns_no_results(self):
        check = SRICheck("https://www.4armed.com")
        html = """<html><head><script src="https://www.4armed.com/script.js"></script></head></html>"""
        remote_resource_tags = check.get_remote_resource_tags(html)
        self.assertEqual(len(remote_resource_tags), 0)
    
    def test_script_tag_on_third_party_with_sri_returns_no_results(self):
        check = SRICheck("https://www.4armed.com")
        html = """<html><head><script crossorigin="anonymous" integrity="sha384-qkIfm9UUNrOzzGFh3YtL/KOHBwDNjW00Iwd0LK/DAsdmiOWRUfXBRl/s1Rtn9h8/" src="https://cdn.cloudflare.com/script.js"></script></head></html>"""
        remote_resource_tags = check.get_remote_resource_tags(html)
        self.assertEqual(len(remote_resource_tags), 0)