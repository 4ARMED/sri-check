#!/usr/bin/env python3

import argparse
import base64
import hashlib
import os
import re
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from importlib import metadata

def generate_sha(remote_resource_tag):
    tag = remote_resource_tag['tag']
    resource_data = requests.get(remote_resource_tag['tag'][remote_resource_tag['attr']]).content
    integrity_checksum = base64.b64encode(hashlib.sha384(resource_data).digest()).decode('utf-8')
    tag['integrity'] = f"sha384-{integrity_checksum}"
    tag['crossorigin'] = 'anonymous'

    return tag

class SRICheck:
    def __init__(self, url):
        self.browser = False
        self.headers = {
            "User-Agent": "4ARMED SRI Check (https://github.com/4armed/sri-check)",
        }
        self.skip_checks = False
        self.stdin = False
        self.verbose = False

        if url == "-":
            self.stdin = True
        elif url == "":
            raise ValueError("URL cannot be empty")
        else:
            parsed_url = urlparse(url)
            if parsed_url.scheme not in {'http', 'https'}:
                raise ValueError("URL must be http or https")
            elif parsed_url.netloc == "":
                raise ValueError("URL must include a hostname")
        
        self.url = url

        # hosts we will ignore (in netloc format), in addition to the target URL
        self.allowlisted_hosts = [
            "fonts\.googleapis\.com", # does not use versioning so can't realistically use SRI
            "fonts\.gstatic\.com", # does not use versioning so can't realistically use SRI
            "js-?[a-z0-9]*\.hs-scripts\.com", # does not use versioning so can't realistically use SRI
            "www\.googletagmanager\.com", # does not use versioning so can't realistically use SRI
        ]           

        if self.stdin is False:
            self.allowlisted_hosts.append(re.escape(urlparse(self.url).netloc))
    
    def set_browser(self, browser):
        self.browser = browser
    
    def set_headers(self, headers):
        self.headers = { 
            **self.headers,
            **headers
        }
    
    def set_stdin(self, stdin):
        self.stdin = stdin
    
    def set_verbose(self, verbose):
        self.verbose = verbose
    
    def add_allowlisted_host(self, pattern):
        self.allowlisted_hosts.append(pattern)
    
    def allowlisted_hosts(self):
        return self.allowlisted_hosts
    
    def set_skip_checks(self, skip_checks):
        self.skip_checks = skip_checks

    def is_allowlisted(self, netloc):
        # Don't check allowlist if skip_checks is True
        if self.skip_checks is True:
            return False
        
        for pattern in self.allowlisted_hosts:
            # file deepcode ignore reDOS: Intended functionality
            if re.search(pattern, netloc):
                return True
            
        return False

    def get_html(self):
        if self.browser:
            from seleniumwire import webdriver

            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.experimental_options["prefs"] = {
                "profile.default_content_settings": {
                    "images": 2
                }
            }

            browser = webdriver.Chrome(
                options=chrome_options,
                seleniumwire_options={
                    'proxy': {
                        'http': os.environ.get("http_proxy"),
                        'https': os.environ.get("https_proxy"),
                    }
                }
            )

            def interceptor(request):
                for key, value in self.headers.items():
                    del request.headers[key]
                    request.headers[key] = value

            browser.request_interceptor = interceptor
            browser.get(self.url)
            content = browser.execute_script("return document.documentElement.outerHTML;")

            browser.quit()
            return content
        else:
            # file deepcode ignore Ssrf: The purpose of the script is to parse remote URLs from the CLI
            return requests.get(self.url, headers=self.headers).content

    def get_remote_resource_tags(self, html):
        soup = BeautifulSoup(html, 'lxml')

        resource_tags = []
        remote_resource_tags = []

        if self.skip_checks is True:
            script_tags = [tag for tag in soup.find_all(['script'], attrs={'src':True})]
            link_tags = [tag for tag in soup.find_all(['link'], attrs={
                'href':True,
                'rel': lambda x: x is not None and x in ['stylesheet', 'preload', 'modulepreload'],
            })]
            resource_tags.extend(script_tags)
            resource_tags.extend(link_tags)
        else:
            script_tags = [tag for tag in soup.find_all(['script'], attrs={'src':True, 'integrity':None})]
            link_tags = [tag for tag in soup.find_all(['link'], attrs={
                'href':True, 
                'integrity':None,
                'rel': lambda x: x is not None and x in ['stylesheet', 'preload', 'modulepreload'],
            })]
            resource_tags.extend(script_tags)
            resource_tags.extend(link_tags)

        if len(resource_tags) > 0:
            parsed_source_url = urlparse(self.url)

            for resource_tag in resource_tags:
                attribute = ""
                for potential_attribute in ['src', 'href']:
                    if potential_attribute in resource_tag.attrs:
                        attribute = potential_attribute

                if re.search('^//', resource_tag[attribute]):
                    resource_tag[attribute] = parsed_source_url.scheme + ':' + resource_tag[attribute]

                parsed_tag = urlparse(resource_tag[attribute])
                if parsed_tag.scheme in {'http', 'https'}:
                    if self.is_allowlisted(parsed_tag.netloc) is False:
                        remote_resource_tags.append({'tag': resource_tag, 'attr': attribute})

        return remote_resource_tags

    def run(self):
        if self.stdin:
            html = sys.stdin.read()
        else:
            html = self.get_html()
        
        if self.verbose is True:
            print(html)

        remote_resource_tags = self.get_remote_resource_tags(html)

        return remote_resource_tags

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--generate", help="Generate sha384 hashes for resources", action="store_true")
    parser.add_argument("-a", "--all", help="Output detected script/link tags regardless of SRI status", action="store_true")
    parser.add_argument("-b", "--browser", help="Use headless browser to retrieve page and run client side rendering", action="store_true")
    parser.add_argument("-H", "--header", help="HTTP header value to send with the request. Specify multiple times if needed", action="append")
    parser.add_argument("-i", "--ignore", help="host to ignore when checking for SRI. e.g. cdn.4armed.com. Specify multiple times if needed", action="append")
    parser.add_argument("-I", "--ignore-regex", help="regex host to ignore when checking for SRI. e.g. .*\.4armed\.com. Specify multiple times if needed", action="append")
    parser.add_argument("-q", "--quiet", help="Suppress output if all tags have SRI (deprecated: now default, use --verbose)", action="store_true")
    parser.add_argument("-z", "--zero-exit", help="Return zero exit code even if tags are found without SRI (default is exit 99)", action="store_true")
    parser.add_argument("-v", "--verbose", help="Enable verbose output", action="store_true")
    parser.add_argument("--version", action="version", version=metadata.version("sri-check"))
    parser.add_argument("url", help="Target URL to check for SRI (use - to read from stdin)")
    args = parser.parse_args()

    try:
        s = SRICheck(url=args.url)
    except ValueError as error:
        print(f"[-] {error}")
        return 1

    headers = {}
    if args.header:
        for header in args.header:
            k, v = header.split(": ")
            headers[k] = v

    if len(headers) > 0:
        s.set_headers(headers)

    s.set_browser(args.browser)
    s.set_verbose(args.verbose)

    if args.ignore:
        for host in args.ignore:
            s.add_allowlisted_host(re.escape(host))

    if args.ignore_regex:
        for pattern in args.ignore_regex:
            s.add_allowlisted_host(pattern)  

    s.set_skip_checks(args.all)
    remote_resource_tags = s.run()

    if len(remote_resource_tags) > 0:
        for remote_resource_tag in remote_resource_tags:
            if args.generate:
                print(generate_sha(remote_resource_tag))
            else:
                print(remote_resource_tag['tag'])
        
        if args.zero_exit is False:
            return 99
    else:
        if args.verbose is True:
            print("[*] No resource tags found without integrity attribute")
        
    return 0

if __name__== "__main__":
    sys.exit(cli())