#!/usr/bin/env python3
"""Static site generator shared by fieldareameasure.com and arazi.app (same code, different content/).

    python3 build.py            # build everything from content/
    python3 build.py --ping     # after deploying: submit all URLs to IndexNow (Bing, Yandex, ...)

content/site.py  : SITE, BRAND, APP_ID, PLAY_ID, LANGS, SISTER, RATING, HOME
content/pages.py : UNITS, EXTRA_UNITS, TOOL, EXTRA_TOOLS, GUIDES, HUB
Generated HTML is committed; GitHub Pages serves the repo root. Legal pages are hand-written.
App screens (assets/img/screen-<lang>-<key>.webp) are real captures of the Android app.
"""
import datetime
import hashlib
import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from content.site import SITE, BRAND, APP_ID, PLAY_ID, LANGS, SISTER, RATING, HOME  # noqa: E402
from content import pages  # noqa: E402

UNITS, TOOL, GUIDES, HUB = pages.UNITS, pages.TOOL, pages.GUIDES, pages.HUB
EXTRA_UNITS = getattr(pages, "EXTRA_UNITS", {})
EXTRA_TOOLS = getattr(pages, "EXTRA_TOOLS", [])
PROVIDER_TOKEN = ""  # App Store Connect → App Analytics → Campaigns
TODAY = datetime.date.today().isoformat()
SUPPORT = "asilarslan93@gmail.com"
HOST = urllib.parse.urlparse(SITE).netloc
INDEXNOW_KEY = hashlib.sha1(("indexnow-" + HOST).encode()).hexdigest()[:32]
esc = html.escape


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)


def version(path):
    return hashlib.sha1(read(path).encode()).hexdigest()[:8]


def exists(path):
    return os.path.exists(os.path.join(ROOT, path))


# ---------------------------------------------------------------- store links

def store_url(campaign):
    q = f"?pt={PROVIDER_TOKEN}&ct={campaign}&mt=8" if PROVIDER_TOKEN else f"?ct={campaign}&mt=8"
    return f"https://apps.apple.com/app/apple-store/id{APP_ID}{q}"


def play_url(campaign):
    ref = urllib.parse.quote(f"utm_source={HOST}&utm_medium=web&utm_campaign={campaign}", safe="")
    return f"https://play.google.com/store/apps/details?id={PLAY_ID}&referrer={ref}"


def svg_width(path, height=54):
    m = re.search(r'<svg[^>]*?width="([\d.]+)"[^>]*?height="([\d.]+)"', read(path)[:600])
    return round(float(m.group(1)) * height / float(m.group(2))) if m else 162


def badge(t, campaign):
    apple = f"assets/img/app-store-{t['badge']}.svg"
    play_w = 164 if t["play"] == "en" else 180
    return (f'<a class="badge" href="{store_url(campaign)}" rel="noopener"><img src="/{apple}" alt="Download on the App Store" '
            f'width="{svg_width(apple)}" height="54"></a><a class="badge" href="{play_url(campaign)}" rel="noopener">'
            f'<img src="/assets/img/play-{t["play"]}.webp" alt="Get it on Google Play" width="{play_w}" height="54"></a>')


def app_link(campaign, cls, inner):
    """App Store link that site.js swaps for Google Play on Android."""
    return f'<a class="{cls}" href="{store_url(campaign)}" data-play="{esc(play_url(campaign))}" rel="noopener">{inner}</a>'


# ---------------------------------------------------------------- shared bits

def home_path(lang):
    return "/" if lang == LANGS[0] else f"/{lang}/"


def slug(path):
    return path.strip("/").replace("/", "-") or "home"


def guides_for(lang):
    own = [g for g in GUIDES if g.get("lang", LANGS[0]) == lang]
    return own or [g for g in GUIDES if g.get("lang", LANGS[0]) == LANGS[0]]


def screen(lang, key):
    for l in (lang, LANGS[0], "en"):
        if exists(f"assets/img/screen-{l}-{key}.webp"):
            return f"/assets/img/screen-{l}-{key}.webp"
    raise SystemExit(f"missing screen {key}")


SCREENS = json.load(open(os.path.join(ROOT, "content", "screens.json")))
SBAR_ICONS = ('<svg width="15" height="11" viewBox="0 0 17 11" aria-hidden="true"><rect x="0" y="7" width="3" height="4" rx="1"/>'
              '<rect x="4.5" y="5" width="3" height="6" rx="1"/><rect x="9" y="2.5" width="3" height="8.5" rx="1"/>'
              '<rect x="13.5" y="0" width="3" height="11" rx="1"/></svg><svg width="22" height="11" viewBox="0 0 25 12" aria-hidden="true">'
              '<rect x=".5" y=".5" width="21" height="11" rx="3" fill="none" stroke="currentColor" opacity=".45"/>'
              '<rect x="2" y="2" width="17" height="8" rx="2"/></svg>')


def device(lang, key, alt, eager=False, cls=""):
    """Real app screenshot (Android status bar cropped) in a phone frame with a clean drawn status bar."""
    src = screen(lang, key)
    m = SCREENS[src.rsplit("screen-", 1)[1].removesuffix(".webp")]
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    ink = "#fff" if m["dark"] else "#0f172a"
    return (f'<div class="device {cls}"><div class="scr" style="background:{m["bg"]}">'
            f'<div class="sbar" style="color:{ink};fill:{ink}"><span>9:41</span><i class="cam"></i><span class="ic">{SBAR_ICONS}</span></div>'
            f'<img src="{src}" alt="{esc(alt)}" width="645" height="{m["h"]}" {load} decoding="async"></div></div>')


def qr(text, cls="qr", size=84):
    return (f'<div class="{cls}"><img src="/assets/img/qr-app-store.svg" alt="QR code" width="{size}" height="{size}" loading="lazy">'
            f'<span>{esc(text)}</span></div>')


def header(lang, alts):
    t = HOME[lang]
    n = t["nav"]
    opts = ""
    if len(LANGS) > 1:
        opts = '<select class="lang" aria-label="Language">' + "".join(
            f'<option value="{alts.get(l, home_path(l))}"{" selected" if l == lang else ""}>{HOME[l]["name"]}</option>' for l in LANGS) + "</select>"
    tool = TOOL[lang]["path"]
    extra = "".join(f'<a class="hide-sm" href="{x["path"]}">{esc(x["nav"])}</a>' for x in EXTRA_TOOLS if x["lang"] == lang)
    return f"""<header class="top"><div class="wrap">
<a class="brand" href="{home_path(lang)}"><img src="/assets/img/icon-64.png" alt="" width="32" height="32">{esc(t.get('brand', BRAND))}</a>
<nav><a class="hide-sm" href="{tool}">{esc(n['tool'])}</a>{extra}<a class="hide-sm" href="{hub_of(lang)['path']}">{esc(n['guides'])}</a>
{opts}{app_link('web-nav-' + lang, 'get', esc(n['get']))}</nav></div></header>"""


def hub_of(lang):
    return HUB.get(lang, HUB) if "path" not in HUB else HUB


def footer(lang):
    t = HOME[lang]
    guides = "".join(f'<li><a href="{g["path"]}">{esc(g["h1"])}</a></li>' for g in guides_for(lang))
    tools = f'<li><a href="{TOOL[lang]["path"]}">{esc(TOOL[lang]["h1"])}</a></li>' + "".join(
        f'<li><a href="{x["path"]}">{esc(x["h1"])}</a></li>' for x in EXTRA_TOOLS if x["lang"] == lang)
    langs = "".join(f'<li><a href="{home_path(l)}" hreflang="{l}">{HOME[l]["name"]}</a></li>' for l in LANGS)
    langs += "".join(f'<li><a href="{u}" hreflang="{l}">{"Türkçe" if l == "tr" else "English"}</a></li>' for l, u in SISTER.items())
    return f"""<footer><div class="wrap cols">
<div><div class="h">{t['footer_app']}</div><ul>
<li><a href="{store_url('web-footer-' + lang)}" rel="noopener">App Store</a></li>
<li><a href="{play_url('web-footer-' + lang)}" rel="noopener">Google Play</a></li>{tools}
<li><a href="mailto:{SUPPORT}">{t['support']}</a></li></ul></div>
<div><div class="h">{t['footer_guides']}</div><ul>{guides}</ul></div>
<div><div class="h">Language</div><ul>{langs}</ul></div>
<div><div class="h">{t['footer_legal']}</div><ul>
<li><a href="/privacy-policy.html">{t['privacy']}</a></li><li><a href="/terms-of-use.html">{t['terms']}</a></li></ul>
<p style="margin-top:12px">© {datetime.date.today().year} {t['copyright']}</p></div>
</div></footer>"""


def sticky(lang, where):
    return f'<div class="sticky-cta">{app_link("web-sticky-" + where, "btn btn-primary", esc(HOME[lang]["sticky"]))}</div>'


def cta_band(lang, where, extra=""):
    t = HOME[lang]
    return f"""<section><div class="wrap"><div class="cta-band">
<h2>{esc(t['cta_h2'])}</h2><p>{esc(t['cta_p'])}</p><div class="ctas">{badge(t, 'web-bottom-' + where)}{extra}</div>
</div></div></section>"""


def faq_html(title, items):
    rows = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in items)
    return f'<h2>{esc(title)}</h2><div class="faq">{rows}</div>'


def ld(obj):
    return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False)}</script>'


def fmt_num(x, lang):
    s = f"{x:,.1f}" if x % 1 else f"{x:,.0f}"
    return s if lang == "en" else s.replace(",", "X").replace(".", ",").replace("X", ".")


def page(lang, title, desc, path, body, *, alternates=None, jsonld=(), preload="", tool=False, og_type="website",
         robots="index, follow, max-image-preview:large"):
    t = HOME[lang]
    url = SITE + path
    alt = ""
    if alternates:
        alt = "".join(f'<link rel="alternate" hreflang="{l}" href="{p if p.startswith("http") else SITE + p}">' for l, p in alternates.items())
        first = alternates.get(LANGS[0])
        if first:
            alt += f'<link rel="alternate" hreflang="x-default" href="{SITE + first}">'
    scripts = f'<script src="/assets/site.js?v={version("assets/site.js")}" defer></script>'
    if tool:
        scripts += f'<script src="/assets/tool.js?v={version("assets/tool.js")}" defer></script>'
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
{alt}
<meta name="robots" content="{robots}">
<meta name="apple-itunes-app" content="app-id={APP_ID}">
<meta name="theme-color" content="#0b1f33">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{esc(t.get('brand', BRAND))}">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE}/assets/img/og-{lang}.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:locale" content="{t['locale']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SITE}/assets/img/og-{lang}.jpg">
<link rel="icon" href="/assets/img/icon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/icon-180.png">
<link rel="manifest" href="/manifest.json">
{preload}
<style>{read('assets/site.css')}</style>
{''.join(ld(j) for j in jsonld)}
</head>
<body>
{body}
{scripts}
</body>
</html>
"""


def app_ld(lang):
    t = HOME[lang]
    ios = {"@context": "https://schema.org", "@type": "MobileApplication", "name": t.get("brand", BRAND),
           "operatingSystem": "iOS", "applicationCategory": "UtilitiesApplication", "url": SITE + home_path(lang),
           "downloadUrl": f"https://apps.apple.com/app/id{APP_ID}", "image": f"{SITE}/assets/img/icon-512.png",
           "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
    if RATING:
        ios["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": str(RATING["value"]),
                                  "ratingCount": str(RATING["count"]), "bestRating": "5", "worstRating": "1"}
    android = {"@context": "https://schema.org", "@type": "MobileApplication", "name": t.get("brand", BRAND),
               "operatingSystem": "Android", "applicationCategory": "UtilitiesApplication", "url": SITE + home_path(lang),
               "downloadUrl": f"https://play.google.com/store/apps/details?id={PLAY_ID}", "image": f"{SITE}/assets/img/icon-512.png",
               "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
    return [ios, android]


ICONS = {
    "tap": '<path d="M9 11V5a2 2 0 0 1 4 0v6"/><path d="M13 9a2 2 0 0 1 4 0v3"/><path d="M17 11a2 2 0 0 1 4 0v4a7 7 0 0 1-7 7h-1a7 7 0 0 1-6-3.4L4 15a2 2 0 0 1 3.4-2L9 15"/>',
    "ruler": '<path d="M3 17 17 3l4 4L7 21z"/><path d="M7 13l2 2M10 10l2 2M13 7l2 2"/>',
    "units": '<path d="M4 4h7v7H4zM13 13h7v7h-7z"/><path d="M13 7h7M17 3v8M4 17h7"/>',
    "pin": '<path d="M12 21s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/>',
    "layers": '<path d="M12 3 2 8l10 5 10-5z"/><path d="M2 13l10 5 10-5"/>',
    "share": '<path d="M12 3v12M7 8l5-5 5 5"/><path d="M5 13v6h14v-6"/>',
    "tractor": '<circle cx="7" cy="17" r="3"/><circle cx="18" cy="18" r="2"/><path d="M4 14V8h7l2 6h5l1-4h-6"/>',
    "home": '<path d="M3 11 12 4l9 7"/><path d="M5 10v10h14V10"/>',
    "compass": '<circle cx="12" cy="12" r="9"/><path d="m15 9-2 5-5 2 2-5z"/>',
    "leaf": '<path d="M5 19C5 9 11 4 20 4c0 9-5 15-15 15z"/><path d="M5 19l8-8"/>',
}
STEP_ICONS = ["pin", "tap", "share"]
WHO_ICONS = ["tractor", "home", "compass", "leaf"]
POINT_ICONS = ["tap", "ruler", "units"]


def icon(name):
    return (f'<svg class="ico" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def kick(t, key):
    return f'<p class="kick">{esc(t["kick"][key])}</p>'


def guide_cards(lang, items=None):
    items = guides_for(lang) if items is None else items
    return "".join(f'<a class="gcard" href="{g["path"]}"><b>{esc(g["h1"])}</b><span>{esc(g["desc"][:110].rsplit(" ", 1)[0])}…</span>'
                   f'<em>→</em></a>' for g in items)


# ---------------------------------------------------------------- pages

def build_home(lang):
    t = HOME[lang]
    a = t["shots_alt"]
    alts = {l: home_path(l) for l in LANGS}
    alts.update(SISTER)
    stats = "".join(f'<div><b>{esc(n)}</b><span>{esc(l)}</span></div>' for n, l in t["stats"])
    points = "".join(f'<li>{icon(POINT_ICONS[i])}<div><b>{esc(x)}</b><p>{esc(y)}</p></div></li>' for i, (x, y) in enumerate(t["measure_points"]))
    site_keys = ["site0", "site1", "site2", "site3"]
    tabs = "".join(f'<div class="stab">{device(lang, site_keys[i], a.get(site_keys[i], a["site0"]), cls="sm")}<h3>{esc(x)}</h3><p>{esc(y)}</p></div>'
                   for i, (x, y) in enumerate(t["site_tabs"]))
    steps = "".join(f'<div class="card">{icon(STEP_ICONS[i])}<h3>{esc(x)}</h3><p>{esc(y)}</p></div>' for i, (x, y) in enumerate(t["steps"]))
    who = "".join(f'<div class="card">{icon(WHO_ICONS[i])}<h3>{esc(x)}</h3><p>{esc(y)}</p></div>' for i, (x, y) in enumerate(t["who"]))
    rating = ""
    if RATING:
        rating = (f'<a class="eyebrow" href="{store_url("web-rating-" + lang)}" rel="noopener"><span class="stars">★★★★★</span> '
                  f'{esc(RATING["label"])}</a>')
    tools = f'<a class="btn btn-ghost light" href="{TOOL[lang]["path"]}">{esc(t["tool_btn"])}</a>'
    body = f"""{header(lang, alts)}
<main>
<section class="hero land" data-hero><div class="wrap">
<div>
{rating}<p class="kick light">{esc(t['kicker'])}</p>
<h1>{esc(t['h1'])}</h1>
<p class="sub">{esc(t['sub'])}</p>
<div class="ctas">{badge(t, 'web-hero-' + lang)}</div>
<p class="compat">{esc(t['compat'])}</p>
<p style="margin-top:16px">{tools}</p>
{qr(t['qr'])}
</div>
<div class="media"><div class="pair">{device(lang, 'site0', a['site0'], cls='back')}{device(lang, 'measure', t['hero_alt'], eager=True, cls='front')}</div></div>
</div></section>
<section class="statbar"><div class="wrap"><div class="stats">{stats}</div></div></section>

<section><div class="wrap split">
<div>{kick(t, 'measure')}<h2>{esc(t['measure_h2'])}</h2><p class="lead">{esc(t['measure_lead'])}</p><ul class="points">{points}</ul></div>
<div class="center">{device(lang, 'measure', a['measure'])}</div>
</div></section>

<section class="alt"><div class="wrap split rev">
<div class="center duo">{device(lang, 'list', a['list'], cls='sm')}{device(lang, 'detail', a['detail'], cls='sm')}</div>
<div><h2>{esc(t['keep_h2'])}</h2><p class="lead">{esc(t['keep_lead'])}</p>
<a class="btn btn-primary" href="{TOOL[lang]['path']}">{esc(t['tool_btn'])}</a></div>
</div></section>

<section class="dark"><div class="wrap">
{kick(t, 'site')}<h2>{esc(t['site_h2'])}</h2><p class="lead">{esc(t['site_lead'])}</p>
<p class="pill">{esc(t['site_note'])}</p>
<div class="stabs">{tabs}</div>
</div></section>

<section><div class="wrap">
{kick(t, 'how')}<h2>{esc(t['how_h2'])}</h2><div class="grid3" style="margin-top:22px">{steps}</div>
<h2 style="margin-top:60px">{esc(t['who_h2'])}</h2><div class="grid4" style="margin-top:22px">{who}</div>
</div></section>

<section class="alt"><div class="wrap">
<div class="inline-cta toolcta">{icon('units')}<p>{esc(t['tool_h2'])}<br><span>{esc(t['tool_p'])}</span></p>
<a class="btn btn-primary" href="{TOOL[lang]['path']}">{esc(t['tool_btn'])}</a></div>
{''.join(f'<div class="inline-cta toolcta">{icon("home")}<p>{esc(x["h1"])}<br><span>{esc(x["desc"][:120].rsplit(" ", 1)[0])}…</span></p><a class="btn btn-primary" href="{x["path"]}">{esc(x["nav"])}</a></div>' for x in EXTRA_TOOLS if x["lang"] == lang)}
{kick(t, 'guides')}<h2>{esc(t['guides_h2'])}</h2><div class="gcards">{guide_cards(lang)}</div>
</div></section>

<section id="faq"><div class="wrap narrow">{kick(t, 'faq')}{faq_html(t['faq_h2'], t['faq'])}</div></section>
{cta_band(lang, lang)}
</main>
{footer(lang)}
{sticky(lang, lang)}"""
    jsonld = [*app_ld(lang), {"@context": "https://schema.org", "@type": "WebSite", "name": t.get("brand", BRAND),
                              "url": SITE + home_path(lang), "inLanguage": lang}]
    out = page(lang, t["title"], t["desc"], home_path(lang), body, alternates=alts, jsonld=jsonld,
               preload=f'<link rel="preload" as="image" href="{screen(lang, "measure")}" fetchpriority="high">')
    write("index.html" if lang == LANGS[0] else f"{lang}/index.html", out)


def article(lang, *, path, title, desc, h1, intro, body_html, faq, alts, kind, top="", shot=None, tool=False, extra_ld=(),
            related=()):
    t = HOME[lang]
    where = slug(path)
    hub = hub_of(lang)
    crumbs = (f'<nav class="crumbs"><a href="{home_path(lang)}">{t["home"]}</a> › '
              + (f'<a href="{hub["path"]}">{t["guides_hub"]}</a> › ' if kind == "guide" else "") + f'{esc(h1)}</nav>')
    side = f'<div class="banner-art">{device(lang, shot, t["shots_alt"].get(shot, h1), eager=True, cls="sm")}</div>' if shot else ""
    updated = f'<p class="upd">{t["updated"]}: {TODAY}</p>' if kind == "guide" else ""
    inline = f'<div class="inline-cta"><p>{esc(t["inline_cta"])}</p>{badge(t, "web-inline-" + where)}</div>'
    rel = ""
    if related:
        rel = f'<section class="alt"><div class="wrap"><h2>{t["related"]}</h2><div class="gcards">{guide_cards(lang, related)}</div></div></section>'
    body = f"""{header(lang, alts)}
<main>
<section class="banner" data-hero><div class="wrap banner-in{' noart' if not shot else ''}">
<div>{crumbs}<h1>{esc(h1)}</h1><p class="intro">{esc(intro)}</p>{updated}</div>{side}
</div></section>
{top}
<section style="padding-top:28px"><div class="wrap narrow prose">
{body_html}
{inline}
<div id="faq">{faq_html(t['faq_h2'], faq) if faq else ''}</div>
</div></section>
{rel}
{cta_band(lang, where, f'<a class="btn btn-ghost" href="{home_path(lang)}">{esc(t["back"])}</a>')}
</main>
{footer(lang)}
{sticky(lang, where)}"""
    crumbs_ld = [{"@type": "ListItem", "position": 1, "name": t["home"], "item": SITE + home_path(lang)}]
    if kind == "guide":
        crumbs_ld.append({"@type": "ListItem", "position": 2, "name": t["guides_hub"], "item": SITE + hub["path"]})
    crumbs_ld.append({"@type": "ListItem", "position": len(crumbs_ld) + 1, "name": h1, "item": SITE + path})
    jsonld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": crumbs_ld}, *extra_ld]
    if kind == "guide":
        jsonld.append({"@context": "https://schema.org", "@type": "Article", "headline": title, "description": desc, "inLanguage": lang,
                       "dateModified": TODAY, "mainEntityOfPage": SITE + path, "image": f"{SITE}/assets/img/og-{lang}.jpg",
                       "author": {"@type": "Organization", "name": t.get("brand", BRAND), "url": SITE + "/"},
                       "publisher": {"@type": "Organization", "name": t.get("brand", BRAND),
                                     "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/img/icon-512.png"}}})
    out = page(lang, title, desc, path, body, alternates=alts if len(alts) > 1 else None, jsonld=jsonld, tool=tool,
               og_type="article" if kind == "guide" else "website")
    write(path.strip("/") + "/index.html", out)


def converter_html(lang):
    tt = TOOL[lang]
    units = [(k, f, lab[lang]) for k, f, lab in UNITS] + list(EXTRA_UNITS.get(lang, []))
    rows = "".join(f'<label class="urow"><span>{esc(lab)}</span><input type="text" inputmode="decimal" data-u="{k}" data-f="{f!r}" '
                   f'autocomplete="off" aria-label="{esc(lab)}"></label>' for k, f, lab in units)
    opts_len = "".join(f'<option value="{v}">{n}</option>' for n, v in (tt.get("len_units") or [("m", 1), ("ft", 0.3048), ("yd", 0.9144)]))
    data = json.dumps({"lang": lang}, ensure_ascii=False)
    return f"""<div class="tool" data-conv>
<script type="application/json" class="tool-i18n">{data}</script>
<div class="ugrid">{rows}</div>
<p class="tnote">{esc(tt['note'])}</p>
</div>
<div class="tool" data-rect style="margin-top:20px">
<h3>{esc(tt['rect_h'])}</h3>
<div class="rgrid"><label>{esc(tt['length'])}<input type="text" inputmode="decimal" data-l></label>
<label>{esc(tt['width'])}<input type="text" inputmode="decimal" data-w></label>
<label>{esc(tt['in_unit'])}<select data-lu>{opts_len}</select></label></div>
<p class="rout" data-rout aria-live="polite"></p>
</div>"""


def build_tool(lang):
    tt = TOOL[lang]
    top = f'<section class="alt" style="padding:32px 0"><div class="wrap narrow">{converter_html(lang)}</div></section>'
    ld_app = {"@context": "https://schema.org", "@type": "WebApplication", "name": tt["h1"], "url": SITE + tt["path"],
              "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any (web browser)", "isAccessibleForFree": True,
              "inLanguage": lang, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
    alts = {l: TOOL[l]["path"] for l in LANGS}
    article(lang, path=tt["path"], title=tt["title"], desc=tt["desc"], h1=tt["h1"], intro=tt["intro"], body_html=tt["body"],
            faq=tt["faq"], alts=alts, kind="tool", top=top, tool=True, extra_ld=[ld_app], related=guides_for(lang)[:3])


def build_extra_tool(x):
    lang = x["lang"]
    top = f'<section class="alt" style="padding:32px 0"><div class="wrap narrow">{x["html"]}</div></section>'
    ld_app = {"@context": "https://schema.org", "@type": "WebApplication", "name": x["h1"], "url": SITE + x["path"],
              "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any (web browser)", "isAccessibleForFree": True,
              "inLanguage": lang, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
    article(lang, path=x["path"], title=x["title"], desc=x["desc"], h1=x["h1"], intro=x["intro"], body_html=x["body"],
            faq=x["faq"], alts={lang: x["path"]}, kind="tool", top=top, tool=True, extra_ld=[ld_app], related=guides_for(lang)[:3])


def build_guide(g):
    lang = g.get("lang", LANGS[0])
    alts = {lang: g["path"], **g.get("alts", {})}
    related = [x for x in guides_for(lang) if x["path"] != g["path"]][:3]
    article(lang, path=g["path"], title=g["title"], desc=g["desc"], h1=g["h1"], intro=g["intro"], body_html=g["body"],
            faq=g["faq"], alts=alts, kind="guide", shot=g.get("shot"), related=related)


def build_hub(lang):
    t = HOME[lang]
    h = hub_of(lang)
    body = f"""{header(lang, {})}
<main>
<section class="banner" data-hero><div class="wrap banner-in noart"><div>
<nav class="crumbs"><a href="{home_path(lang)}">{t['home']}</a> › {esc(h['h1'])}</nav><h1>{esc(h['h1'])}</h1><p class="intro">{esc(h['intro'])}</p>
</div></div></section>
<section><div class="wrap"><div class="gcards">{guide_cards(lang)}</div></div></section>
{cta_band(lang, slug(h['path']))}
</main>
{footer(lang)}
{sticky(lang, slug(h['path']))}"""
    items = [{"@type": "ListItem", "position": i, "url": SITE + g["path"], "name": g["h1"]} for i, g in enumerate(guides_for(lang), 1)]
    write(h["path"].strip("/") + "/index.html", page(lang, h["title"], h["desc"], h["path"], body,
                                                     jsonld=[{"@context": "https://schema.org", "@type": "ItemList", "itemListElement": items}]))


def build_get():
    ios, play = store_url("web-qr"), play_url("web-qr")
    write("get/index.html", f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Get {esc(BRAND)}</title><meta name="robots" content="noindex">
<script>location.replace(/android/i.test(navigator.userAgent) ? {json.dumps(play)} : {json.dumps(ios)});</script>
</head><body style="font-family:-apple-system,sans-serif;text-align:center;padding:40px">
<p><a href="{esc(ios)}">App Store</a> · <a href="{esc(play)}">Google Play</a></p></body></html>
""")


def build_404():
    lang = LANGS[0]
    t = HOME[lang]
    body = f"""{header(lang, {})}
<main><section class="banner"><div class="wrap banner-in noart"><div><h1>404</h1>
<p class="intro"><a href="{home_path(lang)}" style="color:#fff">{esc(t['back'])}</a></p></div></div></section></main>
{footer(lang)}"""
    write("404.html", page(lang, f"404 | {BRAND}", "Page not found.", "/404.html", body, robots="noindex"))


def all_urls():
    e = []
    homes = {l: home_path(l) for l in LANGS}
    e += [(home_path(l), "1.0" if l == LANGS[0] else "0.9", {**homes, **SISTER}) for l in LANGS]
    e += [(TOOL[l]["path"], "0.9", {x: TOOL[x]["path"] for x in LANGS} if len(LANGS) > 1 else {}) for l in LANGS]
    e += [(x["path"], "0.9", {}) for x in EXTRA_TOOLS]
    hubs = {hub_of(l)["path"] for l in LANGS}
    e += [(p, "0.6", {}) for p in sorted(hubs)]
    e += [(g["path"], "0.8", {}) for g in GUIDES]
    e += [("/privacy-policy.html", "0.3", {}), ("/terms-of-use.html", "0.3", {})]
    return e


def build_meta():
    rows = []
    for path, prio, alts in all_urls():
        x = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{p if p.startswith("http") else SITE + p}"/>' for l, p in alts.items())
        if alts and LANGS[0] in alts:
            x += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{alts[LANGS[0]]}"/>'
        rows.append(f"  <url>\n    <loc>{SITE}{path}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <priority>{prio}</priority>{x}\n  </url>")
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
          'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(rows) + "\n</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    write(f"{INDEXNOW_KEY}.txt", INDEXNOW_KEY)
    write("manifest.json", json.dumps({
        "name": HOME[LANGS[0]].get("brand", BRAND), "short_name": HOME[LANGS[0]].get("brand", BRAND),
        "start_url": "/", "display": "browser", "background_color": "#ffffff", "theme_color": "#0b1f33",
        "icons": [{"src": "/assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}],
        "related_applications": [{"platform": "itunes", "url": f"https://apps.apple.com/app/id{APP_ID}"},
                                 {"platform": "play", "id": PLAY_ID, "url": f"https://play.google.com/store/apps/details?id={PLAY_ID}"}],
    }, indent=2) + "\n")


def ping_indexnow():
    body = json.dumps({"host": HOST, "key": INDEXNOW_KEY, "keyLocation": f"{SITE}/{INDEXNOW_KEY}.txt",
                       "urlList": [SITE + p for p, _, _ in all_urls()]}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
    print("IndexNow:", urllib.request.urlopen(req, timeout=20).status)


def main():
    if "--ping" in sys.argv:
        return ping_indexnow()
    for lang in LANGS:
        build_home(lang)
        build_tool(lang)
    for x in EXTRA_TOOLS:
        build_extra_tool(x)
    for lang in sorted({g.get("lang", LANGS[0]) for g in GUIDES}):
        build_hub(lang)
    for g in GUIDES:
        build_guide(g)
    build_get()
    build_404()
    build_meta()
    print(f"{HOST}: {len(LANGS)} languages, {len(GUIDES)} guides, {1 + len(EXTRA_TOOLS)} tools")


if __name__ == "__main__":
    main()
