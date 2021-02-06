#!/usr/bin/env python3

import argparse
import base64
import hashlib
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

parser = argparse.ArgumentParser()
parser.add_argument("-g", "--generate", help="Generate sha384 hashes for resources", action="store_true")
parser.add_argument("-a", "--all", help="Output detected script/link tags regardless of SRI status", action="store_true")
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
    resource_tags = [tag for tag in soup.find_all(['script', 'link'], attrs={'src':True})]
else:
    resource_tags = [tag for tag in soup.find_all(['script', 'link'], attrs={'src':True, 'integrity':None})]

if len(resource_tags) > 0:
    remote_resource_tags = []
    generated_resource_tags = []

    for resource_tag in resource_tags:
        parsed_tag = urlparse(resource_tag['src'])
        if parsed_tag.scheme in {'http', 'https'}:
            remote_resource_tags.append(resource_tag)

    if len(remote_resource_tags) > 0:
        if args.generate:
            print("[*] Resource tags without SRI:\n")

        for remote_resource_tag in remote_resource_tags:
            print(remote_resource_tag)

            if args.generate:
                generated_resource_tags.append(generate_sha(remote_resource_tag))
    else:
        print("[*] No resource tags found without integrity attribute")


    if len(generated_resource_tags) > 0:
        print("\n[*] Generated SRIs:\n")
        for generated_resource_tag in generated_resource_tags:
            print(generated_resource_tag)
