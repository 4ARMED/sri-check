# SRI Checker

Ridiculously simple Python script for grabbing `<script>` tags from a remote URL and outputting any that don't have an `integrity` attribute for Subresource Integrity.

We use it for <a href="https://www.4armed.com/assess/penetration-testing/">application security reviews</a> but you can use it for whatever you like!

## Install

You need a few libraries. There's a `requirements.txt` file in this repo for use with pip. We recommend using a venv to isolate these dependencies.

If you use the `Makefile` it will set one up for you.

```bash
$ make
Requirement already satisfied: beautifulsoup4==4.9.3 in /usr/local/lib/python3.9/site-packages (from -r requirements.txt (line 1)) (4.9.3)
Requirement already satisfied: certifi==2020.12.5 in /usr/local/lib/python3.9/site-packages (from -r requirements.txt (line 2)) (2020.12.5)
Requirement already satisfied: chardet==4.0.0 in /usr/local/lib/python3.9/site-packages (from -r requirements.txt (line 3)) (4.0.0)
Requirement already satisfied: idna==2.10 in /usr/local/lib/python3.9/site-packages (from -r requirements.txt (line 4)) (2.10)
Requirement already satisfied: requests==2.25.1 in /usr/local/lib/python3.9/site-packages (from -r requirements.txt (line 5)) (2.25.1)
Requirement already satisfied: soupsieve==2.1 in /usr/local/lib/python3.9/site-packages (from -r requirements.txt (line 6)) (2.1)
Requirement already satisfied: urllib3==1.26.3 in /usr/local/lib/python3.9/site-packages (from -r requirements.txt (line 7)) (1.26.3)
Now run source venv/bin/activate
```

Alternatively you can run the commands yourself.

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Usage

### Check

Now you can run the script which in its most basic form takes one argument, the URL you wish to check.

```bash
$ ./sri-check https://kubernetes.io/
<script async="" src="https://www.googletagmanager.com/gtag/js?id=UA-36037335-10"></script>
<script async="" src="https://www.google-analytics.com/analytics.js"></script>
<link href="https://kubernetes.io/zh/" hreflang="zh" rel="alternate"/>
<link href="https://kubernetes.io/ko/" hreflang="ko" rel="alternate"/>
<link href="https://kubernetes.io/ja/" hreflang="ja" rel="alternate"/>
<link href="https://kubernetes.io/fr/" hreflang="fr" rel="alternate"/>
<link href="https://kubernetes.io/it/" hreflang="it" rel="alternate"/>
<link href="https://kubernetes.io/de/" hreflang="de" rel="alternate"/>
<link href="https://kubernetes.io/es/" hreflang="es" rel="alternate"/>
<link href="https://kubernetes.io/pt/" hreflang="pt" rel="alternate"/>
<link href="https://kubernetes.io/id/" hreflang="id" rel="alternate"/>
<link href="https://kubernetes.io/vi/" hreflang="vi" rel="alternate"/>
<link href="https://kubernetes.io/ru/" hreflang="ru" rel="alternate"/>
<link href="https://kubernetes.io/pl/" hreflang="pl" rel="alternate"/>
<link href="https://kubernetes.io/uk/" hreflang="uk" rel="alternate"/>
<link href="https://kubernetes.io/feed.xml" rel="alternate" type="application/rss+xml"/>
<link href="https://cdn-images.mailchimp.com/embedcode/horizontal-slim-10_7.css" rel="stylesheet" type="text/css"/>
```

> Sidenote: Don't worry about tags which aren't versioned, like the analytics ones above. You will spin your wheels trying to track changes and update the SRI hash.

If the page you are checking requires some kind of authorisation, you can specify HTTP request headers using the `--header` or `-H` flag.

```bash
$ ./sri-check -H "Authorization: Bearer mytoken" -H "More: Headers" https://kubernetes.io/
```

### Generate

Optionally you may wish to output updated script tags with the SRI hash calculated. You can do this by specifying the `--generate` flag.

```bash
$ ./sri-check --generate https://kubernetes.io/
[*] Script tags without SRI:

<script async="" src="https://www.googletagmanager.com/gtag/js?id=UA-36037335-10"></script>
<script async="" src="https://www.google-analytics.com/analytics.js"></script>

[*] Generated SRIs:

<script async="" crossorigin="anonymous" integrity="sha384-ITXXO4YR2TnoUD5vtyrbRhklkt/Q9hFZILlBvnQfLCe4dFJzAofF5sflCksWtNRa" src="https://www.googletagmanager.com/gtag/js?id=UA-36037335-10"></script>
<script async="" crossorigin="anonymous" integrity="sha384-+Mufq/JopHTZLYFkTpT8TA9y0zY/A/VflmpyMsbjcGbcyUbfudhn5Et/w6EIFhoo" src="https://www.google-analytics.com/analytics.js"></script>
```