#!/usr/bin/env python3

import requests
import bs4
import sys
from urllib.parse import urlparse

if len(sys.argv) > 1:
    target_url = sys.argv[1]
else:
    print(f"[!] Usage: {sys.argv[0]} <url>")
    sys.exit(1)

html = requests.get(target_url).content
soup = bs4.BeautifulSoup(html, features='html.parser')
script_tags = [tag for tag in soup.find_all('script', attrs={'src':True, 'integrity':None})]

if len(script_tags) > 0:
    remote_script_tags = []
    for script_tag in script_tags:
        parsed_tag = urlparse(script_tag['src'])
        if parsed_tag.scheme in {'http', 'https'}:
            remote_script_tags.append(script_tag)

    if len(remote_script_tags) > 0:
        for remote_script_tag in remote_script_tags:
            print(remote_script_tag)
    else:
        print("[*] no script tags found without integrity attribute")