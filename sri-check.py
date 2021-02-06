#!/usr/bin/env python3

import argparse
import base64
import hashlib
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

parser = argparse.ArgumentParser()
parser.add_argument("-g", "--generate", help="Generate sha384 hashes for script tags", action="store_true")
parser.add_argument("-a", "--all", help="Output detected script tags regardless of SRI status", action="store_true")
parser.add_argument("url", help="Target URL to check for SRI")
args = parser.parse_args()

def generate_sha(tag):
    resource_data = requests.get(tag['src']).content
    integrity_checksum = base64.b64encode(hashlib.sha384(resource_data).digest()).decode('utf-8')
    tag['integrity'] = f"sha384-{integrity_checksum}"
    tag['crossorigin'] = 'anonymous'

    return tag

html = requests.get(args.url).content
soup = BeautifulSoup(html, features='html.parser')
if args.all:
    script_tags = [tag for tag in soup.find_all('script', attrs={'src':True})]
else:
    script_tags = [tag for tag in soup.find_all('script', attrs={'src':True, 'integrity':None})]

if len(script_tags) > 0:
    remote_script_tags = []
    generated_script_tags = []

    for script_tag in script_tags:
        parsed_tag = urlparse(script_tag['src'])
        if parsed_tag.scheme in {'http', 'https'}:
            remote_script_tags.append(script_tag)

    if len(remote_script_tags) > 0:
        if args.generate:
            print("[*] Script tags without SRI:\n")

        for remote_script_tag in remote_script_tags:
            print(remote_script_tag)

            if args.generate:
                generated_script_tags.append(generate_sha(remote_script_tag))
    else:
        print("[*] No script tags found without integrity attribute")


    if len(generated_script_tags) > 0:
        print("\n[*] Generated SRIs:\n")
        for generated_script_tag in generated_script_tags:
            print(generated_script_tag)
