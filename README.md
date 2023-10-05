# SRI Checker

Ridiculously simple Python script for grabbing resource tags (script, link) from a remote URL and outputting any that don't have an `integrity` attribute for Subresource Integrity.

We use it for <a href="https://www.4armed.com/assess/penetration-testing/">application security reviews</a> but you can use it for whatever you like!

## Install

The easiest way is to install it from PyPi using:

```bash
pip install sri-check
```

Then you should have `sri-check` in your PATH.

## Usage

### Check

Now you can run the script which in its most basic form takes one argument, the URL you wish to check.
```bash
sri-check https://www.4armed.com/
<script src="https://cdn.jsdelivr.net/npm/swiper@7.4.1/swiper-bundle.min.js"></script>
<link href="https://use.typekit.net/vlp2azz.css" rel="stylesheet"/>
<link href="https://cdn.jsdelivr.net/npm/swiper@7.4.1/swiper-bundle.min.css" rel="stylesheet"/>
```

Tut, tut, you can see above that on our website we have a few external dependencies without SRI.

If sri-check finds any tags missing SRI that it will output, it also returns a non-zero exit code (99). In this way you can use sri-check in pipelines or scripts if you wish. I've included the dollar signs here to differentiate the shell commands from the output.

```bash
$ sri-check https://www.4armed.com/
<script src="https://cdn.jsdelivr.net/npm/swiper@7.4.1/swiper-bundle.min.js"></script>
<link href="https://use.typekit.net/vlp2azz.css" rel="stylesheet"/>
<link href="https://cdn.jsdelivr.net/npm/swiper@7.4.1/swiper-bundle.min.css" rel="stylesheet"/>
$ echo $?
99
```

### Allowlisting

Allowlisting is a way to tell sri-check that this _host_ is ok. By default sri-check adds the target host to the allow list, as well as some common third-party analytics domains which do not use versioning (Google, Hubspot, etc).

In the example above, the 4ARMED website is using typekit CSS for its fonts. Since this isn't a versioned resource if we generate an integrity hash for it and implement SRI, it could legitimately change and break the fonts. We'd either have to monitor this and update the hash or decide to accept this.

To add this host to the allow list we use the `--ignore` or `-i` flag and sri-check won't report it.

```bash
sri-check -i use.typekit.net https://www.4armed.com/
<script src="https://cdn.jsdelivr.net/npm/swiper@7.4.1/swiper-bundle.min.js"></script>
<link href="https://cdn.jsdelivr.net/npm/swiper@7.4.1/swiper-bundle.min.css" rel="stylesheet"/>
```

That's a bit cleaner. But what if we want to ignore multiple hosts? You can specify multiple `-i` flags.

```bash
sri-check -i use.typekit.net -i cdn.jsdelivr.net https://www.4armed.com/
[*] No resource tags found without integrity attribute
```

In this case, there are no SRI concerns left to report so sri-check tells you. If you don't want output if there's nothing to worry about you can use the `-q` flag to tell sri-check to be quiet.

```bash
sri-check -i use.typekit.net -i cdn.jsdelivr.net https://www.4armed.com/ -q
```

Let's have a look at another example now, the BBC News site.

```bash
sri-check https://www.bbc.co.uk/news/
<script nomodule="" src="https://static.files.bbci.co.uk/orbit/33bd882d2f5b902e64a28e50d337afa4/js/polyfills.js" type="text/javascript"></script>
<script src="https://static.files.bbci.co.uk/orbit/33bd882d2f5b902e64a28e50d337afa4/js/require.min.js"></script>
<script src="https://static.files.bbci.co.uk/cookies/1098fb404f038cacf92f0ee250c025a0/cookie-banner/cookie-library.bundle.js"></script>
<script async="" src="https://mybbc-analytics.files.bbci.co.uk/reverb-client-js/reverb-3.8.0.js" type="text/javascript"></script>
<script defer="" src="https://m.files.bbci.co.uk/modules/bbc-morph-news-breaking-news-banner/2.1.2/breakingNewsBanner.js"></script>
<script src="https://m.files.bbci.co.uk/modules/bbc-morph-news-local-slice/2.10.6/xss.min.js"></script>
<script class="js-asset-path" data-asset-path="//m.files.bbci.co.uk/modules/bbc-morph-news-local-slice/2.10.6/" data-slice-path="/news/local_news_slice/" defer="" src="https://m.files.bbci.co.uk/modules/bbc-morph-news-local-slice/2.10.6/main.min.js"></script>
<script async="" src="https://static.files.bbci.co.uk/orbit/33bd882d2f5b902e64a28e50d337afa4/js/redirect.js" type="text/javascript"></script>
<script async="" data-release="3.0.1-208.5a547360" data-ux="v5" src="https://static.files.bbci.co.uk/orbit/33bd882d2f5b902e64a28e50d337afa4/js/performance.js" type="text/javascript"></script>
<script src="https://static.files.bbci.co.uk/orbit/33bd882d2f5b902e64a28e50d337afa4/js/more-drawer.mjs" type="module"></script>
<script async="" src="https://static.files.bbci.co.uk/orbit/33bd882d2f5b902e64a28e50d337afa4/js/orbit.mjs" type="module"></script>
<script async="" nomodule="" src="https://static.files.bbci.co.uk/orbit/33bd882d2f5b902e64a28e50d337afa4/js/orbit.js" type="text/javascript"></script>
<script async="" data-base="https://navpromo.api.bbci.co.uk" data-variant="default" src="https://nav.files.bbci.co.uk/navpromo/f67a9538931d75e28d1807a3daf6dc00/js/footerpromo.js" type="text/javascript"></script>
<script async="" src="https://static.files.bbci.co.uk/cookies/1098fb404f038cacf92f0ee250c025a0/cookie-banner/cookie-banners.bundle.js"></script>
<script async="" src="https://nav.files.bbci.co.uk//user-activity-helper/a029a4d9f7f005262e2e6043630347b3/js/detectview.bundle.js"></script>
<script defer="defer" src="https://mybbc.files.bbci.co.uk/notification-ui/5.0.25//js/NotificationsMain.js"></script>
<script async="" src="https://m.files.bbci.co.uk/modules/bbc-morph-news-front-page-js-bundle/1.56.4/newsFrontPagePersonalised.js"></script>
<link crossorigin="" href="https://static.bbc.co.uk" rel="preconnect"/>
<link crossorigin="" href="https://m.files.bbci.co.uk" rel="preconnect"/>
<link crossorigin="" href="https://nav.files.bbci.co.uk" rel="preconnect"/>
<link crossorigin="" href="https://ichef.bbci.co.uk" rel="preconnect"/>
<link href="https://mybbc.files.bbci.co.uk" rel="dns-prefetch"/>
<link href="https://ssl.bbc.co.uk/" rel="dns-prefetch"/>
<link href="https://sa.bbc.co.uk/" rel="dns-prefetch"/>
<link href="https://ichef.bbci.co.uk" rel="dns-prefetch"/>
<link as="style" href="https://m.files.bbci.co.uk/modules/bbc-morph-news-page-styles/2.4.25/enhanced.css" rel="preload"/>
<link href="https://www.bbc.com/news" hreflang="en" rel="alternate"/>
<link href="https://m.files.bbci.co.uk/modules/bbc-morph-news-waf-page-meta/5.3.0/apple-touch-icon-57x57-precomposed.png" rel="apple-touch-icon-precomposed" sizes="57x57"/>
<link href="https://m.files.bbci.co.uk/modules/bbc-morph-news-waf-page-meta/5.3.0/apple-touch-icon-72x72-precomposed.png" rel="apple-touch-icon-precomposed" sizes="72x72"/>
<link href="https://m.files.bbci.co.uk/modules/bbc-morph-news-waf-page-meta/5.3.0/apple-touch-icon-114x114-precomposed.png" rel="apple-touch-icon-precomposed" sizes="114x114"/>
<link href="https://m.files.bbci.co.uk/modules/bbc-morph-news-waf-page-meta/5.3.0/apple-touch-icon.png" rel="apple-touch-icon-precomposed" sizes="144x144"/>
<link href="https://m.files.bbci.co.uk/modules/bbc-morph-news-waf-page-meta/5.3.0/apple-touch-icon.png" rel="apple-touch-icon"/>
<link href="https://static.files.bbci.co.uk/orbit/33bd882d2f5b902e64a28e50d337afa4/css/orbit-v5-ltr.min.css" rel="stylesheet"/>
<link as="font" crossorigin="" href="https://static.files.bbci.co.uk/fonts/reith/2.512/BBCReithSans_W_Rg.woff2" rel="preload" type="font/woff2"/>
<link as="font" crossorigin="" href="https://static.files.bbci.co.uk/fonts/reith/2.512/BBCReithSans_W_Bd.woff2" rel="preload" type="font/woff2"/>
<link href="https://nav.files.bbci.co.uk/searchbox/521fdb102453edfd515ee5fca2a40eda/css/box.css" rel="stylesheet"/>
<link href="https://static.files.bbci.co.uk/account/id-cta/621/style/id-cta.css" rel="stylesheet"/>
<link href="https://m.files.bbci.co.uk/modules/bbc-morph-news-page-styles/2.4.25/core.css" rel="stylesheet"/>
```

Woah, they've got a lot of resources without SRI. Although.... on closer inspection, a lot of those URLs seem to be their own hosts, so they're probably not too worried about putting SRI on them. So we can sri-check to ignore these hosts but there's quite a few. `nav.files.bbci.co.uk`, `sa.bbc.co.uk`, etc. To help with this, sri-check also supports the `--ignore-regex` or `-I` flag.

```bash
sri-check -I '.*\.bbci\.co\.uk' https://www.bbc.co.uk/news/
<link crossorigin="" href="https://static.bbc.co.uk" rel="preconnect"/>
<link href="https://ssl.bbc.co.uk/" rel="dns-prefetch"/>
<link href="https://sa.bbc.co.uk/" rel="dns-prefetch"/>
<link href="https://www.bbc.com/news" hreflang="en" rel="alternate"/>
```

That's looking pretty good. The ones which are left are also BBC domains. We could tweak our regex or just add a couple more `-I` flags.

```bash
sri-check -I '.*\.bbci\.co\.uk' -I '.*\.bbc\.co[m|\.uk]' https://www.bbc.co.uk/news/
[*] No resource tags found without integrity attribute
```

Nice.

### Headers

If the page you are checking requires some kind of authorisation, you can specify HTTP request headers using the `--header` or `-H` flag.

```bash
$ sri-check -H "Authorization: Bearer mytoken" -H "More: Headers" https://www.4armed.com/
```

### Headless Browser

By default, sri-check uses the Python requests library to fetch the remote resources. In case you are working with SPA application where external resources may be dynamically written into the DOM and therefore not be visible in the source HTML, you can use a headless Chrome browser to render page before running check by setting `--browser` or `-b` flag.

### Generating Hashes

If you decide you want to fix these resources and implement SRI, sri-check can output the required tags for you, computing a SHA384 integrity hash for each resource. Use the `--generate` or -`-g` flag.

```bash
sri-check -i use.typekit.net https://www.4armed.com/ -g
<script crossorigin="anonymous" integrity="sha384-uZ9tjGJYBp5yJzyGlqrVDWn2thY23HUzI9DhkhNhYa+6xmG2kvy3S28S5r4yE7cN" src="https://cdn.jsdelivr.net/npm/swiper@7.4.1/swiper-bundle.min.js"></script>
<link crossorigin="anonymous" href="https://cdn.jsdelivr.net/npm/swiper@7.4.1/swiper-bundle.min.css" integrity="sha384-uh3y/WeAusiZJ76/oewz8WiTiOl0SIQXYOTNT42NZ65y/Hyo8j3qGw7dnVAmSSDn" rel="stylesheet"/>
```

### STDIN

sri-check also supports reading input from STDIN, like all good CLI tools. :-) Simply specify the target URL as `-` to do this. It means you could pipe the output of curl through it, for example. 

```bash
curl -s https://www.4armed.com/ | sri-check -
<script src="https://cdn.jsdelivr.net/npm/swiper@7.4.1/swiper-bundle.min.js"></script>
<link href="https://use.typekit.net/vlp2azz.css" rel="stylesheet"/>
<link href="https://cdn.jsdelivr.net/npm/swiper@7.4.1/swiper-bundle.min.css" rel="stylesheet"/>
```

Or you might have some HTML you've saved from somewhere into a file.

```bash
cat /tmp/4armed.html | sri-check -
<script src="https://cdn.jsdelivr.net/npm/swiper@7.4.1/swiper-bundle.min.js"></script>
<link href="https://use.typekit.net/vlp2azz.css" rel="stylesheet"/>
<link href="https://cdn.jsdelivr.net/npm/swiper@7.4.1/swiper-bundle.min.css" rel="stylesheet"/>
```

