#!/usr/bin/env python3
"""Static site generator for kitchen.daveys.xyz.

Writes ./public from content/*.py. Stdlib only: `python3 generator/build.py`.
"""
from __future__ import annotations

import html
import json
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
OUT = ROOT / "public"

from content.ingredients import CATEGORIES, INGREDIENTS  # noqa: E402
from content.tables import (GENERAL_CONVERSIONS, OVEN, PAN_DIAMETERS_IN,  # noqa: E402
                            PAN_NOTES, UNIT_SYSTEMS, VOLUME_MEASURES)

# ----------------------------------------------------------------- configuration
SITE = "https://kitchen.daveys.xyz"
SITE_NAME = "Kitchen Conversions"
TAGLINE = "Cups, grams, oven temperatures and pan sizes — measured properly"
TODAY = date.today().isoformat()

# AdSense placeholder. Set this to the publisher ID (eg "ca-pub-1234567890123456") and the
# meta tag plus the in-page ad units become live; leave it empty and every page still carries
# an inert .adslot marker where the units will go.
ADSENSE_CLIENT = ""
ADSENSE_SLOTS = {
    "top": "0000000000",     # under the h1, before the tool
    "mid": "1111111111",     # after the reference table
    "bottom": "2222222222",  # before the FAQ
}

US_CUP_ML = 236.5882365
PAGES: list[dict] = []


# ----------------------------------------------------------------- helpers
def e(text: object) -> str:
    return html.escape(str(text), quote=False)


def url(path: str) -> str:
    return SITE + path


def fmt(value: float, decimals: int = 0) -> str:
    out = f"{value:,.{decimals}f}"
    if decimals and "." in out:
        out = out.rstrip("0").rstrip(".")
    return out


def cup_amounts() -> list[tuple[str, float]]:
    return [("1/8 cup", 0.125), ("1/4 cup", 0.25), ("1/3 cup", 1 / 3), ("1/2 cup", 0.5),
            ("2/3 cup", 2 / 3), ("3/4 cup", 0.75), ("1 cup", 1.0), ("1 1/2 cups", 1.5),
            ("2 cups", 2.0), ("3 cups", 3.0), ("4 cups", 4.0)]


def to_fraction(value: float) -> str:
    """Nearest everyday kitchen fraction, for cup amounts."""
    if value <= 0:
        return "0"
    whole = int(value)
    rest = value - whole
    table = [(0.0, ""), (0.125, "1/8"), (0.25, "1/4"), (1 / 3, "1/3"), (0.375, "3/8"),
             (0.5, "1/2"), (0.625, "5/8"), (2 / 3, "2/3"), (0.75, "3/4"), (0.875, "7/8"),
             (1.0, "")]
    best_gap, best = 1.0, ""
    for frac, label in table:
        gap = abs(frac - rest)
        if gap < best_gap:
            best_gap, best = gap, label
    out = str(whole) if whole else ""
    if best:
        out = (out + " " + best).strip()
    if best_gap > 0.04:
        out = "≈ " + out if out else out
    return out or "0"


def ad_slot(key: str) -> str:
    slot = ADSENSE_SLOTS[key]
    if ADSENSE_CLIENT:
        return (f'<div class="adslot"><ins class="adsbygoogle" style="display:block"'
                f' data-ad-client="{ADSENSE_CLIENT}" data-ad-slot="{slot}"'
                f' data-ad-format="auto" data-full-width-responsive="true"></ins>'
                f'<script>(adsbygoogle=window.adsbygoogle||[]).push({{}});</script></div>')
    return f'<div class="adslot" data-ad-placeholder="{key}"><!-- ad slot "{key}" --></div>'


def crumbs(items: list[tuple[str, str]]) -> str:
    if not items:
        return ""
    parts = [f'<a href="{href}">{e(label)}</a>' for label, href in items]
    return f'<nav class="crumbs">{" › ".join(parts)}</nav>'


def page(path: str, title: str, description: str, body: str,
         crumb: list[tuple[str, str]] | None = None,
         jsonld: list[dict] | None = None,
         priority: float = 0.6) -> None:
    PAGES.append({"path": path, "priority": priority, "title": title, "description": description})
    head_extra = ""
    if ADSENSE_CLIENT:
        head_extra = (f'\n<meta name="google-adsense-account" content="{ADSENSE_CLIENT}">'
                      f'\n<script async src="https://pagead2.googlesyndication.com/pagead/js/'
                      f'adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>')
    else:
        head_extra = ('\n<!-- AdSense placeholder: set ADSENSE_CLIENT in generator/build.py -->')

    ld = "\n".join(
        f'<script type="application/ld+json">{json.dumps(block, separators=(",", ":"))}</script>'
        for block in (jsonld or []))

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{url(path)}">{head_extra}
<link rel="stylesheet" href="/assets/style.css">
<script src="/assets/consent.js" defer></script>
<script src="/assets/app.js" defer></script>
{ld}
</head>
<body>
<header class="site"><div class="wrap">
<a class="brand" href="/">{e(SITE_NAME)}</a>
<nav>
<a href="/cups-to-grams/">Cups to grams</a>
<a href="/oven-temperatures/">Oven</a>
<a href="/pan-sizes/">Pans</a>
<a href="/volume/">Volume</a>
</nav>
</div></header>
<main><div class="wrap">
{crumbs(crumb or [])}
{body}
</div></main>
<footer class="site"><div class="wrap">
<p>{e(SITE_NAME)} — reference tables and converters for cooking measurements.
Weights follow King Arthur Baking's ingredient weight chart; conversions are computed, not
copied.</p>
<p><a href="/about/">About</a><a href="/methodology/">How these numbers are sourced</a>
<a href="/privacy/">Privacy</a><a href="/contact/">Contact</a></p>
</div></footer>
</body>
</html>
"""
    target = OUT / path.strip("/") if path != "/" else OUT
    if path.endswith("/"):
        target = OUT / path.strip("/") / "index.html"
    else:
        target = OUT / path.lstrip("/")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(doc, encoding="utf8")


def converter(factor: float, from_label: str, to_label: str, note: str = "",
              from_decimals: int = 4, to_decimals: int = 0, fraction_out: bool = False,
              default_from: str = "1") -> str:
    frac_html = '<p class="hint" id="frac">In cups: <strong class="frac-out"></strong></p>' \
        if fraction_out else ""
    return f"""<div class="card">
<div class="converter" data-factor="{factor}" data-from-decimals="{from_decimals}"
     data-to-decimals="{to_decimals}"{f' data-fraction="to"' if fraction_out else ''}>
  <div><label for="c-from">{e(from_label)}</label>
    <input id="c-from" data-role="from" type="text" inputmode="decimal" value="{default_from}"
           autocomplete="off"></div>
  <div class="swap">⇄</div>
  <div><label for="c-to">{e(to_label)}</label>
    <input id="c-to" data-role="to" type="text" inputmode="decimal" autocomplete="off"></div>
</div>
{frac_html}
{f'<p class="hint">{e(note)}</p>' if note else ''}
</div>"""


def temp_converter(mode: str, from_label: str, to_label: str, default: float = 180) -> str:
    return f"""<div class="card">
<div class="converter" data-mode="{mode}">
  <div><label for="t-from">{e(from_label)}</label>
    <input id="t-from" data-role="from" type="text" inputmode="decimal" value="{fmt(default)}"
           autocomplete="off"></div>
  <div class="swap">⇄</div>
  <div><label for="t-to">{e(to_label)}</label>
    <input id="t-to" data-role="to" type="text" inputmode="decimal" autocomplete="off"></div>
</div>
<p class="hint">Both boxes are live — type in either one.</p>
</div>"""


def units_widget(system: str, label: str) -> str:
    """A value + unit-from + unit-to converter, used on the conversions hub."""
    units = UNIT_SYSTEMS[system]["units"]
    data = json.dumps(units, separators=(",", ":"))
    return f"""<div class="card"><h3>{e(label)}</h3>
<div class="converter" data-units='{data}'>
  <div><label for="u-{system}">Value</label>
    <input id="u-{system}" data-role="unit-value" type="text" inputmode="decimal" value="1"
           autocomplete="off"></div>
  <div class="swap">⇄</div>
  <div><label for="uf-{system}">From</label><select id="uf-{system}" data-role="unit-from"></select></div>
  <div><label for="ut-{system}">To</label><select id="ut-{system}" data-role="unit-to"></select></div>
</div>
<p class="hint">Equals <strong data-role="unit-out"></strong></p></div>"""


def faq(items: list[tuple[str, str]]) -> str:
    blocks = "".join(f"<h3>{e(q)}</h3><p>{a}</p>" for q, a in items)
    return f'<section class="faq"><h2>Common questions</h2>{blocks}</section>'


def faq_ld(items: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": q2}}
                       for q, q2 in items],
    }


def breadcrumb_ld(items: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": label,
                             "item": url(href)}
                            for i, (label, href) in enumerate(items)],
    }


# ----------------------------------------------------------------- home
def build_home() -> None:
    cards = [
        ("/cups-to-grams/", "Cups to grams",
         "By ingredient — flour, sugar, butter, honey and 32 more"),
        ("/grams-to-cups/", "Grams to cups", "The same ingredients, the other way round"),
        ("/oven-temperatures/", "Oven temperatures",
         "Celsius, Fahrenheit, fan and gas mark in one table"),
        ("/pan-sizes/", "Pan sizes and substitutions",
         "Round, square, inches, centimetres, and what will fit"),
        ("/volume/", "Volume measures", "US cups against metric cups, spoons and pints"),
        ("/recipe-scaler/", "Recipe scaler", "Multiply or divide a recipe's quantities"),
    ]
    grid = "".join(f'<a href="{href}">{e(t)}<span>{e(s)}</span></a>' for href, t, s in cards)
    body = f"""
<h1>Cooking conversions, measured properly</h1>
<p class="lede">Cups to grams by ingredient, oven temperatures, pan sizes and volume
measures — with the numbers explained rather than just converted.</p>
{ad_slot("top")}
<p>A cup of flour is not a fixed amount. Spooned and levelled it weighs about 120&nbsp;g;
scooped straight from the bag it can weigh over 150&nbsp;g, and that difference is enough to
turn a good cake into a dry one. That is why this site gives weights <em>per ingredient</em>
rather than pretending a cup is a cup.</p>
<div class="grid">{grid}</div>
<h2>Where the numbers come from</h2>
<p>Ingredient weights follow <a href="https://www.kingarthurbaking.com/learn/ingredient-weight-chart"
rel="nofollow">King Arthur Baking's ingredient weight chart</a>, one of the few published
charts that states its measuring convention. Unit conversions are computed from the
definitions — an inch is 2.54&nbsp;cm exactly, a US cup is 236.588&nbsp;ml — so rounding
only ever happens in what is displayed. See <a href="/methodology/">how these numbers are
sourced</a>.</p>
{ad_slot("bottom")}
"""
    page("/", f"{SITE_NAME} — cups to grams, oven temperatures, pan sizes",
         "Convert cups to grams by ingredient, oven temperatures between Celsius, Fahrenheit, "
         "fan and gas mark, pan sizes and volume measures — with the numbers properly sourced.",
         body,
         jsonld=[{"@context": "https://schema.org", "@type": "WebSite",
                  "name": SITE_NAME, "url": SITE}],
         priority=1.0)


# ----------------------------------------------------------------- ingredients
def ingredient_tables(ing: dict) -> tuple[str, str]:
    g = ing["g"]
    up = "".join(
        f'<tr><td>{label}</td><td class="num">{fmt(cups * g)} g</td>'
        f'<td class="num">{fmt(cups * g / 28.349523125, 1)} oz</td></tr>'
        for label, cups in cup_amounts())
    grams = [10, 20, 25, 50, 75, 100, 125, 150, 200, 250, 300, 400, 500]
    down = "".join(
        f'<tr><td class="num">{amount} g</td>'
        f'<td class="num">{fmt(amount / g, 2)}</td>'
        f'<td>{to_fraction(amount / g)} cup</td></tr>'
        for amount in grams)
    return up, down


def build_ingredient_pages() -> None:
    by_cat: dict[str, list[dict]] = {key: [] for key, _, _ in CATEGORIES}
    for ing in INGREDIENTS:
        by_cat[ing["cat"]].append(ing)

    hub_cards = ""
    for key, label, blurb in CATEGORIES:
        items = "".join(
            f'<a href="/cups-to-grams/{i["slug"]}/">{e(i["name"])}<span>{fmt(i["g"])} g per US '
            f'cup</span></a>' for i in by_cat[key])
        hub_cards += (f'<h2>{e(label)}</h2><p class="note">{e(blurb)}</p>'
                      f'<div class="grid">{items}</div>')

    hub_body = f"""
<h1>Cups to grams, by ingredient</h1>
<p class="lede">Choose an ingredient for its own conversion tables — weights, ounces and
fractions of a cup, using the measuring convention each chart actually states.</p>
{ad_slot("top")}
<p>Sugar measures the same whoever fills the cup. Flour does not. Below, every ingredient has
its own page with a two-way converter, a cups-to-grams table and a grams-to-cups table, so you
can work in whichever direction your recipe is written.</p>
{hub_cards}
"""
    page("/cups-to-grams/", "Cups to grams converter — by ingredient",
         "Cups to grams for 36 ingredients: flour, sugar, butter, honey, oats, cocoa and more. "
         "Two-way converters and full reference tables.", hub_body, priority=0.9)

    reverse_cards = ""
    for key, label, _ in CATEGORIES:
        items = "".join(
            f'<a href="/grams-to-cups/{i["slug"]}/">{e(i["name"])}<span>{fmt(i["g"])} g per US '
            f'cup</span></a>' for i in by_cat[key])
        reverse_cards += f'<h2>{e(label)}</h2><div class="grid">{items}</div>'

    page("/grams-to-cups/", "Grams to cups converter — by ingredient",
         "Grams to cups for 36 ingredients, with a two-way converter and reference tables. "
         "Built for recipes written in weight.",
         f"""
<h1>Grams to cups, by ingredient</h1>
<p class="lede">If your recipe is in grams and your cups are the only measure you have, start
here.</p>
{ad_slot("top")}
<p>Dividing by the ingredient's weight per cup gives an answer in cups, and the tables also
show the nearest everyday fraction — because 0.42 of a cup is not a useful instruction.</p>
{reverse_cards}
""", priority=0.8)

    for ing in INGREDIENTS:
        g = ing["g"]
        up_table, down_table = ingredient_tables(ing)
        name = ing["name"]
        crumbs_up = [("Cups to grams", "/cups-to-grams/"), (name, f"/cups-to-grams/{ing['slug']}/")]
        crumbs_down = [("Grams to cups", "/grams-to-cups/"), (name, f"/grams-to-cups/{ing['slug']}/")]

        # ---- cups -> grams
        faqs_up = [
            (f"How many grams is 1 cup of {ing['short']}?",
             f"A US cup of {ing['short']} weighs about <strong>{fmt(g)} grams</strong> when "
             f"measured the way the reference charts measure it — spooned into the cup and "
             f"levelled. Using a metric cup of 250&nbsp;ml instead raises that by about 5.6%, "
             f"to roughly {fmt(g * 250 / US_CUP_ML)}&nbsp;g."),
            (f"How many grams is half a cup of {ing['short']}?",
             f"About {fmt(g / 2)}&nbsp;g ({fmt(g / 2 / 28.349523125, 1)}&nbsp;oz). Halving the "
             f"volume halves the weight — unlike the cup itself, weight has no measuring "
             f"convention to argue about."),
            (f"Is a cup of {ing['short']} the same in the US and the UK?",
             f"No. A US customary cup is 236.588&nbsp;ml; the metric cup used in the UK, "
             f"Australia, New Zealand and Canada is 250&nbsp;ml, and the old imperial cup was "
             f"284&nbsp;ml. For {ing['short']} those are roughly {fmt(g)}, "
             f"{fmt(g * 250 / US_CUP_ML)} and {fmt(g * 284.130625 / US_CUP_ML)}&nbsp;g."),
        ]
        body_up = f"""
<h1>How many grams in a cup of {e(ing['short'])}?</h1>
<p class="lede">One US cup of {e(name.lower())} weighs about <strong>{fmt(g)}&nbsp;g</strong>
({fmt(g / 28.349523125, 1)}&nbsp;oz) when spooned and levelled.</p>
{ad_slot("top")}
{converter(g, "cups", "grams", "Type either box; the other updates as you type. Based on a US "
                        "customary cup of 236.588 ml.", from_decimals=3, to_decimals=0)}
<h2>Cups to grams for {e(ing['short'])}</h2>
<table>
<thead><tr><th>Cups</th><th class="num">Grams</th><th class="num">Ounces</th></tr></thead>
<tbody>{up_table}</tbody>
</table>
{ad_slot("mid")}
<h2>Why the number is not fixed</h2>
<p>{e(ing['note'])}</p>
<h2>How to measure it</h2>
<p>{e(ing['tip'])}</p>
{faq(faqs_up)}
<p class="note">Working the other way? See <a href="/grams-to-cups/{ing['slug']}/">grams to cups
for {e(ing['short'])}</a>.</p>
{ad_slot("bottom")}
"""
        page(f"/cups-to-grams/{ing['slug']}/",
             f"Cups to grams: {name} — converter and table",
             f"How many grams in a cup of {ing['short']}? About {fmt(g)} g. Two-way converter, "
             f"cups-to-grams table in grams and ounces, and measuring guidance.",
             body_up, crumb=crumbs_up, jsonld=[faq_ld(faqs_up), breadcrumb_ld(crumbs_up)],
             priority=0.7)

        # ---- grams -> cups
        faqs_down = [
            (f"How many cups is {fmt(round(g, -1))} grams of {ing['short']}?",
             f"{fmt(round(g, -1))}&nbsp;g is about {fmt(round(g, -1) / g, 2)} cups, or "
             f"{to_fraction(round(g, -1) / g)} in kitchen terms."),
            (f"How do I convert grams of {ing['short']} to cups without scales?",
             f"Divide the grams by {fmt(g)} — the weight of one US cup — and then round to the "
             f"nearest measure you have. A set of cups marked in eighths will cover almost "
             f"every recipe."),
        ]
        body_down = f"""
<h1>Grams to cups: {e(ing['short'])}</h1>
<p class="lede">Divide grams by {fmt(g)} to get US cups — or use the converter, which gives
the fraction as well.</p>
{ad_slot("top")}
{converter(1 / g, "grams", "cups", "Type either box; the other updates as you type.",
           from_decimals=0, to_decimals=3, fraction_out=True, default_from=str(g))}
<h2>Grams to cups for {e(ing['short'])}</h2>
<table>
<thead><tr><th class="num">Grams</th><th class="num">Cups (decimal)</th><th>Cups (fraction)</th></tr></thead>
<tbody>{down_table}</tbody>
</table>
{ad_slot("mid")}
<h2>Why {e(ing['short'])} is measured this way</h2>
<p>{e(ing['note'])}</p>
<h2>Measuring without scales</h2>
<p>{e(ing['tip'])}</p>
{faq(faqs_down)}
<p class="note">Working the other way? See <a href="/cups-to-grams/{ing['slug']}/">cups to grams
for {e(ing['short'])}</a>.</p>
{ad_slot("bottom")}
"""
        page(f"/grams-to-cups/{ing['slug']}/",
             f"Grams to cups: {name} — converter and table",
             f"Convert grams of {ing['short']} to cups: {fmt(g)} g per US cup, with a two-way "
             f"converter and a grams-to-cups reference table including fractions.",
             body_down, crumb=crumbs_down,
             jsonld=[faq_ld(faqs_down), breadcrumb_ld(crumbs_down)], priority=0.7)


# ----------------------------------------------------------------- oven
def build_oven_pages() -> None:
    rows = "".join(
        f'<tr><td class="num">{c} °C</td><td class="num">{f} °F</td>'
        f'<td class="num">{c - 20}</td><td class="num">{gas}</td><td>{e(use)}</td></tr>'
        for c, gas, f, use in OVEN)
    hub = f"""
<h1>Oven temperature conversions</h1>
<p class="lede">Celsius, Fahrenheit, fan (convection) and gas mark — in one table, with the
formula underneath it.</p>
{ad_slot("top")}
<p>Most ovens are less accurate than the dial suggests: domestic thermostats commonly run
10–20&nbsp;°C out either way, and fan ovens are usually set about 20&nbsp;°C lower than the
equivalent conventional temperature. If a bake is consistently wrong in the same direction,
trust the oven thermometer over the table.</p>
<h2>The full conversion table</h2>
<table>
<thead><tr><th class="num">Conventional</th><th class="num">Fahrenheit</th>
<th class="num">Fan °C</th><th class="num">Gas mark</th><th>Typical use</th></tr></thead>
<tbody>{rows}</tbody>
</table>
<p class="note">Fan values use the usual rule of thumb of 20&nbsp;°C below the conventional
temperature. Gas marks are a British convention, not a conversion.</p>
<h2>The formulas</h2>
<p>Fahrenheit = (Celsius × 9 ÷ 5) + 32. Celsius = (Fahrenheit − 32) × 5 ÷ 9. Those are exact;
only the display is rounded.</p>
<div class="grid">
<a href="/oven-temperatures/celsius-to-fahrenheit/">Celsius to Fahrenheit<span>Converter and table</span></a>
<a href="/oven-temperatures/fahrenheit-to-celsius/">Fahrenheit to Celsius<span>Converter and table</span></a>
<a href="/oven-temperatures/fan-oven/">Fan oven conversion<span>Fan vs conventional</span></a>
<a href="/oven-temperatures/gas-marks/">Gas marks<span>Gas 1 to gas 9 in Celsius and Fahrenheit</span></a>
</div>
{ad_slot("bottom")}
"""
    page("/oven-temperatures/", "Oven temperature conversions — C, F, fan and gas mark",
         "Convert oven temperatures between Celsius, Fahrenheit, fan and gas mark, with a full "
         "table and the exact formulas.", hub, priority=0.9)

    def simple(name: str, slug: str, mode: str, from_l: str, to_l: str, intro: str,
               rows_html: str, extra: str = "") -> None:
        crumb = [("Oven temperatures", "/oven-temperatures/"), (name, f"/oven-temperatures/{slug}/")]
        body = f"""
<h1>{e(name)}</h1>
<p class="lede">{intro}</p>
{ad_slot("top")}
<div class="card"><div class="converter" data-mode="{mode}">
  <div><label for="t-from">{e(from_l)}</label>
    <input id="t-from" data-role="from" type="text" inputmode="decimal" value="180" autocomplete="off"></div>
  <div class="swap">⇄</div>
  <div><label for="t-to">{e(to_l)}</label>
    <input id="t-to" data-role="to" type="text" inputmode="decimal" autocomplete="off"></div>
</div><p class="hint">Both boxes are live — type in either one.</p></div>
{rows_html}
{extra}
"""
        page(f"/oven-temperatures/{slug}/", f"{name} — converter and table",
             f"{intro} Full reference table and live converter.", body, crumb=crumb,
             jsonld=[breadcrumb_ld(crumb)], priority=0.6)

    c2f_rows = "".join(
        f'<tr><td class="num">{c} °C</td><td class="num">{f} °F</td>'
        f'<td class="num">{c - 20} °C fan</td><td class="num">{gas}</td></tr>'
        for c, gas, f, _ in OVEN)
    simple("Celsius to Fahrenheit", "celsius-to-fahrenheit", "c2f", "Celsius (°C)",
           "Fahrenheit (°F)",
           "Multiply by 9, divide by 5, add 32 — that is the whole conversion.",
           "<h2>Common oven temperatures</h2><table><thead><tr><th class='num'>Celsius</th>"
           "<th class='num'>Fahrenheit</th><th class='num'>Fan</th><th class='num'>Gas</th>"
           f"</tr></thead><tbody>{c2f_rows}</tbody></table>")

    f2c_rows = "".join(
        f'<tr><td class="num">{f} °F</td><td class="num">{c} °C</td></tr>'
        for c, _, f, _ in OVEN)
    simple("Fahrenheit to Celsius", "fahrenheit-to-celsius", "f2c", "Fahrenheit (°F)",
           "Celsius (°C)",
           "Subtract 32, multiply by 5, divide by 9. American recipes are usually written in "
           "Fahrenheit, which is why a 350 °F recipe is really a 180 °C one.",
           "<h2>Common oven temperatures</h2><table><thead><tr><th class='num'>Fahrenheit</th>"
           f"<th class='num'>Celsius</th></tr></thead><tbody>{f2c_rows}</tbody></table>")

    fan_rows = "".join(
        f'<tr><td class="num">{c - 20} °C fan</td><td class="num">{c} °C conventional</td>'
        f'<td class="num">{f} °F</td></tr>' for c, _, f, _ in OVEN)
    simple("Fan oven conversion", "fan-oven", "fan", "Fan (°C)", "Conventional (°C)",
           "A fan oven moves air, so it cooks hotter and faster: set it about 20 °C lower than "
           "a conventional recipe asks for.",
           "<h2>Fan against conventional</h2><table><thead><tr><th class='num'>Fan</th>"
           "<th class='num'>Conventional</th><th class='num'>Fahrenheit</th></tr></thead>"
           f"<tbody>{fan_rows}</tbody></table><p class='note'>If your oven only does fan, drop "
           "the temperature 20 °C and check five to ten minutes earlier than the recipe "
           "suggests. If it only does conventional and the recipe is written for fan, raise it "
           "20 °C.</p>")

    gas_rows = "".join(
        f'<tr><td class="num">{gas}</td><td class="num">{c} °C</td><td class="num">{f} °F</td>'
        f'<td>{e(use)}</td></tr>' for c, gas, f, use in OVEN if gas != "1/4" and gas != "1/2")
    simple("Gas marks", "gas-marks", "c2f", "Celsius (°C)", "Fahrenheit (°F)",
           "Gas marks are a British oven convention, not a unit of temperature — gas 4 is "
           "350 °F, which is 180 °C.",
           "<h2>Gas marks in Celsius and Fahrenheit</h2><table><thead><tr>"
           "<th class='num'>Gas</th><th class='num'>°C</th><th class='num'>°F</th>"
           f"<th>Typical use</th></tr></thead><tbody>{gas_rows}</tbody></table>")

    for c, gas, f, use in OVEN:
        crumb = [("Oven temperatures", "/oven-temperatures/"),
                 (f"{c} °C", f"/oven-temperatures/{c}c-to-f/")]
        nearby = "".join(
            f'<tr><td class="num">{cc} °C</td><td class="num">{ff} °F</td>'
            f'<td class="num">{cc - 20} °C fan</td><td class="num">{gg}</td></tr>'
            for cc, gg, ff, _ in OVEN if abs(cc - c) <= 40)
        body = f"""
<h1>{c} °C in Fahrenheit</h1>
<p class="lede">{c} °C is <strong>{f} °F</strong>. On a fan oven set it to about
{c - 20} °C, and on a British gas cooker it is gas mark {gas}.</p>
{ad_slot("top")}
{temp_converter("c2f", "Celsius (°C)", "Fahrenheit (°F)", c)}
<h2>What {c} °C is used for</h2>
<p>{e(use)}. Centigrade and Celsius are the same scale — the unit was renamed in 1948 after
Anders Celsius, who had originally defined it upside down, with 0 as boiling.</p>
<h2>Nearby temperatures</h2>
<table><thead><tr><th class="num">Celsius</th><th class="num">Fahrenheit</th>
<th class="num">Fan</th><th class="num">Gas</th></tr></thead><tbody>{nearby}</tbody></table>
<p class="note">Full table: <a href="/oven-temperatures/">all oven temperature conversions</a>.</p>
"""
        page(f"/oven-temperatures/{c}c-to-f/", f"{c} °C to °F — oven temperature conversion",
             f"{c} °C is {f} °F: {c - 20} °C in a fan oven, gas mark {gas}. Converter, use and "
             f"nearby temperatures.", body, crumb=crumb, jsonld=[breadcrumb_ld(crumb)],
             priority=0.5)

    for mark in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        match = [row for row in OVEN if row[1] == mark]
        if not match:
            continue
        c, gas, f, use = match[0]
        crumb = [("Oven temperatures", "/oven-temperatures/"),
                 (f"Gas mark {mark}", f"/oven-temperatures/gas-mark-{mark}/")]
        body = f"""
<h1>Gas mark {mark} in Celsius and Fahrenheit</h1>
<p class="lede">Gas mark {mark} is <strong>{c} °C</strong> or <strong>{f} °F</strong>, and about
{c - 20} °C in a fan oven.</p>
{ad_slot("top")}
<h2>What it is for</h2>
<p>{e(use)}.</p>
<h2>Gas marks nearby</h2>
<table><thead><tr><th class="num">Gas</th><th class="num">°C</th><th class="num">°F</th>
<th class="num">Fan °C</th></tr></thead><tbody>
{"".join(f'<tr><td class="num">{g}</td><td class="num">{cc}</td><td class="num">{ff}</td><td class="num">{cc - 20}</td></tr>' for cc, g, ff, _ in OVEN if g.isdigit() and abs(int(g) - int(mark)) <= 2)}
</tbody></table>
<p class="note">Gas marks are a British convention tied to the old gas ovens: each mark raises
the temperature in roughly even steps from gas 1 to gas 9.</p>
"""
        page(f"/oven-temperatures/gas-mark-{mark}/",
             f"Gas mark {mark} — {c} °C / {f} °F",
             f"Gas mark {mark} equals {c} °C and {f} °F, or {c - 20} °C in a fan oven. "
             f"{e(use)}.", body, crumb=crumb, jsonld=[breadcrumb_ld(crumb)], priority=0.5)


# ----------------------------------------------------------------- pans
def build_pan_pages() -> None:
    rows = []
    for d in PAN_DIAMETERS_IN:
        cm = d * 2.54
        area = 3.141592653589793 * (d / 2) ** 2
        depth = 2.0
        volume_ml = area * depth * 16.387064
        rows.append((d, cm, area, volume_ml))
    table = "".join(
        f'<tr><td class="num">{d} in</td><td class="num">{fmt(cm, 1)} cm</td>'
        f'<td class="num">{fmt(area)} in²</td><td class="num">{fmt(volume_ml / US_CUP_ML, 1)} cups</td>'
        f'<td class="num">{fmt(volume_ml / 1000, 1)} l</td></tr>' for d, cm, area, volume_ml in rows)

    hub = f"""
<h1>Pan sizes: inches to centimetres and substitutions</h1>
<p class="lede">What a 9-inch tin is in centimetres, what it holds, and what else will fit
instead.</p>
{ad_slot("top")}
<p>Pan sizes are quoted by the manufacturer's rim, so an "8-inch" tin is often 20&nbsp;cm
across the base and rather more across the top. For substitution, area matters more than
diameter: an 8-inch round and an 8-inch square are not the same, but a 9-inch round and an
8-inch square very nearly are.</p>
<h2>Common round tins</h2>
<table><thead><tr><th class="num">Diameter</th><th class="num">Metric</th>
<th class="num">Area</th><th class="num">Capacity (2 in deep)</th><th class="num">Litres</th></tr></thead>
<tbody>{table}</tbody></table>
<p class="note">Capacity is the cylinder's volume — a real cake tin is filled about half to
two&nbsp;thirds, so a 9-inch tin holds a 7-cup batch comfortably.</p>
<div class="grid">
{"".join(f'<a href="/pan-sizes/{d}-inch-pan/">{d} inch pan<span>{fmt(d * 2.54, 1)} cm across</span></a>' for d in PAN_DIAMETERS_IN)}
<a href="/pan-sizes/round-to-square/">Round to square<span>The substitution that works</span></a>
</div>
{ad_slot("bottom")}
"""
    page("/pan-sizes/", "Pan sizes — inches to cm, areas and substitutions",
         "Convert pan sizes between inches and centimetres, compare areas, and find "
         "substitutions that will actually fit.", hub, priority=0.8)

    for d in PAN_DIAMETERS_IN:
        cm = d * 2.54
        area = 3.141592653589793 * (d / 2) ** 2
        square_side = area ** 0.5
        equivalents = [(dd, 3.141592653589793 * (dd / 2) ** 2) for dd in PAN_DIAMETERS_IN]
        nearby = "".join(
            f'<tr><td class="num">{dd} in ({fmt(dd * 2.54, 1)} cm)</td>'
            f'<td class="num">{fmt(a)} in²</td>'
            f'<td>{"a little smaller" if a < area else "a little larger" if a > area else "identical"}</td></tr>'
            for dd, a in equivalents)
        crumb = [("Pan sizes", "/pan-sizes/"), (f"{d} inch pan", f"/pan-sizes/{d}-inch-pan/")]
        body = f"""
<h1>{d} inch pan in centimetres</h1>
<p class="lede">A {d}-inch tin is <strong>{fmt(cm, 1)} cm</strong> across, with an area of
about {fmt(area)} square inches.</p>
{ad_slot("top")}
<h2>What it holds</h2>
<p>At two inches deep, a {d}-inch round tin has a volume of roughly
{fmt(3.141592653589793 * (d / 2) ** 2 * 2 * 16.387064 / US_CUP_ML, 1)} cups of batter. Cakes are
normally baked in a tin filled between half and two thirds, so allow for that rather than
filling it.</p>
<p>{e(PAN_NOTES.get(d, ""))}</p>
<h2>Substituting a {d}-inch tin</h2>
<p>The nearest square tin to a {d}-inch round has sides of about {fmt(square_side, 1)} inches,
because a square has no wasted rim. For a {d}-inch round recipe, an 8-inch square is the
classic American equivalence.</p>
<table><thead><tr><th>Tin</th><th class="num">Area</th><th>Compared with a {d} in round</th></tr></thead>
<tbody>{nearby}</tbody></table>
<h2>Timing when you substitute</h2>
<p>A larger pan means a shallower cake, which bakes faster; a smaller one means a deeper cake
and a longer bake. As a rule, drop the oven 10&nbsp;°C and start checking five minutes earlier
when using a bigger tin, and add five to ten minutes for a smaller, deeper one.</p>
"""
        page(f"/pan-sizes/{d}-inch-pan/", f"{d} inch pan in cm — size, area and substitutions",
             f"A {d} inch pan is {fmt(cm, 1)} cm across. Area, capacity in cups, and which other "
             f"pan sizes will work in its place.", body, crumb=crumb,
             jsonld=[breadcrumb_ld(crumb)], priority=0.5)

    sub_rows = "".join(
        f'<tr><td>{s} in square ({fmt(s * 2.54, 1)} cm)</td>'
        f'<td class="num">{fmt(s * s)} in²</td>'
        f'<td>{fmt(2 * s / 3.141592653589793 ** 0.5, 1)} in round '
        f'({fmt(2 * s / 3.141592653589793 ** 0.5 * 2.54, 1)} cm)</td></tr>'
        for s in PAN_DIAMETERS_IN)
    crumb = [("Pan sizes", "/pan-sizes/"), ("Round to square", "/pan-sizes/round-to-square/")]
    body = f"""
<h1>Round to square: pan substitutions</h1>
<p class="lede">A round tin loses batter to the corners; a square one does not. Match the
areas, not the widths.</p>
{ad_slot("top")}
<p>An 8-inch square tin has an area of 64 square inches. An 8-inch round has 50.3, and a
9-inch round has 63.6 — which is why a 9-inch round is the standard substitute for an 8-inch
square, and why swapping an 8-inch round for an 8-inch square gives you a shallower cake.</p>
<table><thead><tr><th>Round tin</th><th class="num">Area (in²)</th><th>Nearest equivalent</th></tr></thead>
<tbody>{sub_rows}</tbody></table>
<p class="note">Square tins also expose more surface to the oven's heat, so bakes brown a
little faster in the corners. Drop the temperature by 10&nbsp;°C and check early the first
time.</p>
"""
    page("/pan-sizes/round-to-square/", "Round to square pan substitution — matching areas",
         "How to swap between round and square cake tins by matching area: 9-inch round equals "
         "8-inch square, with a full table.", body, crumb=crumb, jsonld=[breadcrumb_ld(crumb)],
         priority=0.5)


# ----------------------------------------------------------------- volume
def build_volume_pages() -> None:
    rows = "".join(
        f'<tr><td>{e(name)}</td><td class="num">{fmt(ml / US_CUP_ML, 3)} US cups</td>'
        f'<td class="num">{fmt(ml, 3)} ml</td><td>{e(note)}</td></tr>'
        for name, ml, note in VOLUME_MEASURES)
    hub = f"""
<h1>Volume measures for cooking</h1>
<p class="lede">A US cup is 236.588&nbsp;ml. A metric cup is 250&nbsp;ml. A UK pint is 20%
larger than an American one. This is the table that keeps them apart.</p>
{ad_slot("top")}
<table><thead><tr><th>Measure</th><th class="num">In US cups</th><th class="num">Millilitres</th>
<th>Note</th></tr></thead><tbody>{rows}</tbody></table>
<h2>The measurement that catches most people out</h2>
<p>Cups are not universal. The United States uses a cup of 236.588&nbsp;ml defined as eight US
fluid ounces. Britain, Australia, New Zealand and Canada increasingly use a 250&nbsp;ml metric
cup, and British cookbooks written before the metric changeover often meant an imperial cup of
284&nbsp;ml. Between the smallest and largest that is a 20% difference, which is a real
difference in a cake.</p>
<div class="grid">
<a href="/volume/us-cups-in-ml/">US cups in ml<span>236.588 ml exactly</span></a>
<a href="/volume/metric-cups-in-ml/">Metric cups in ml<span>250 ml</span></a>
<a href="/volume/tablespoons/">Tablespoons<span>US, UK and Australian</span></a>
<a href="/volume/us-vs-uk-cups/">US vs UK cups<span>Side by side</span></a>
<a href="/volume/us-vs-uk-pints/">US vs UK pints<span>20% apart</span></a>
<a href="/recipe-scaler/">Recipe scaler<span>Halve or double a recipe</span></a>
</div>
{ad_slot("bottom")}
"""
    page("/volume/", "Cooking volume measures — cups, ml, spoons and pints",
         "US, UK and metric cups in millilitres, tablespoons and teaspoons compared, and why a "
         "cup is not a cup.", hub, priority=0.8)

    def vol_page(slug: str, title: str, lede: str, body_lines: list[str]) -> None:
        crumb = [("Volume", "/volume/"), (title, f"/volume/{slug}/")]
        body = f"<h1>{e(title)}</h1>\n<p class=\"lede\">{lede}</p>\n{ad_slot('top')}\n" + \
               "\n".join(body_lines)
        page(f"/volume/{slug}/", f"{title} — cooking measures",
             lede, body, crumb=crumb, jsonld=[breadcrumb_ld(crumb)], priority=0.5)

    vol_page("us-cups-in-ml", "US cups in millilitres",
             "One US cup is <strong>236.588 ml</strong> — 8 US fluid ounces, 16 tablespoons.",
             ["<h2>Converting a recipe written in US cups</h2>",
              "<table><thead><tr><th>Cups</th><th class=\"num\">Millilitres</th>"
              "<th class=\"num\">US fl oz</th></tr></thead><tbody>" +
              "".join(f'<tr><td>{label}</td><td class="num">{fmt(cups * US_CUP_ML, 1)}</td>'
                      f'<td class="num">{fmt(cups * 8, 1)}</td></tr>'
                      for label, cups in cup_amounts()) +
              "</tbody></table>",
              "<p>A millilitre of water weighs a gram, but a millilitre of flour is about half a "
              "gram and a millilitre of honey is about 1.4 grams. Volume conversions between "
              "liquids are safe; between dry ingredients they are not — use the "
              "<a href=\"/cups-to-grams/\">per-ingredient weights</a> instead.</p>"])

    vol_page("metric-cups-in-ml", "Metric cups in millilitres",
             "A metric cup is <strong>250 ml</strong> — a round number, and 5.6% larger than the "
             "US cup.",
             ["<h2>Cups by country</h2>",
              "<table><thead><tr><th>Cup</th><th class=\"num\">Millilitres</th>"
              "<th>Used in</th></tr></thead><tbody>"
              "<tr><td>US customary</td><td class=\"num\">236.588</td><td>United States recipes</td></tr>"
              "<tr><td>Metric</td><td class=\"num\">250</td><td>UK, Australia, New Zealand, Canada "
              "(modern recipes)</td></tr>"
              "<tr><td>Imperial</td><td class=\"num\">284.131</td><td>Older British cookbooks</td></tr>"
              "<tr><td>Japanese</td><td class=\"num\">200</td><td>Japanese recipes (1 ごう = 180 ml)</td></tr>"
              "</tbody></table>",
              "<p>When a British recipe says a cup, assume 250&nbsp;ml unless it was written for "
              "an American audience or specifies US cups. The 13&nbsp;ml difference rarely "
              "matters for liquid but does for flour, where 250&nbsp;ml is about 127&nbsp;g "
              "against 120&nbsp;g.</p>"])

    vol_page("tablespoons", "Tablespoons and teaspoons in millilitres",
             "A US tablespoon is <strong>14.787 ml</strong>. A UK one is 15&nbsp;ml. An "
             "Australian one is 20&nbsp;ml.",
             ["<h2>Spoons compared</h2>",
              "<table><thead><tr><th>Spoon</th><th class=\"num\">Millilitres</th>"
              "<th class=\"num\">Teaspoons</th></tr></thead><tbody>"
              "<tr><td>US teaspoon</td><td class=\"num\">4.929</td><td class=\"num\">1</td></tr>"
              "<tr><td>US tablespoon</td><td class=\"num\">14.787</td><td class=\"num\">3</td></tr>"
              "<tr><td>UK/EU tablespoon</td><td class=\"num\">15</td><td class=\"num\">3 (UK "
              "teaspoon 5 ml)</td></tr>"
              "<tr><td>Australian tablespoon</td><td class=\"num\">20</td><td class=\"num\">4</td></tr>"
              "</tbody></table>",
              "<p>An Australian tablespoon holds a third more than a British one, and the "
              "difference matters most with raising agents, where a third more baking powder "
              "changes the rise. Recipes written in Australia usually say so.</p>"])

    vol_page("us-vs-uk-cups", "US cups against UK cups",
             "236.588&nbsp;ml against 250&nbsp;ml — and 284&nbsp;ml if the book is old enough.",
             ["<h2>Side by side</h2>",
              "<table><thead><tr><th>Ingredient</th><th class=\"num\">1 US cup</th>"
              "<th class=\"num\">1 metric cup</th><th class=\"num\">Difference</th></tr></thead><tbody>" +
              "".join(
                  f'<tr><td>{e(i["name"])}</td><td class="num">{fmt(i["g"])} g</td>'
                  f'<td class="num">{fmt(i["g"] * 250 / US_CUP_ML)} g</td>'
                  f'<td class="num">+{fmt(i["g"] * 250 / US_CUP_ML - i["g"], 1)} g</td></tr>'
                  for i in INGREDIENTS if i["cat"] in ("flours", "sugars")) +
              "</tbody></table>",
              "<p>For liquids the difference is 13.4&nbsp;ml a cup, which is under a tablespoon "
              "and rarely worth worrying about. For flour it is about 7&nbsp;g, and for a four-cup "
              "recipe that is 28&nbsp;g — enough to change a cake.</p>"])

    vol_page("us-vs-uk-pints", "US pints against UK pints",
             "A British pint is 568.261&nbsp;ml. An American pint is 473.176&nbsp;ml — 20% "
             "smaller.",
             ["<h2>Side by side</h2>",
              "<table><thead><tr><th>Measure</th><th class=\"num\">US</th><th class=\"num\">UK "
              "imperial</th></tr></thead><tbody>"
              "<tr><td>Fluid ounce</td><td class=\"num\">29.574 ml</td><td class=\"num\">28.413 ml</td></tr>"
              "<tr><td>Pint (16 / 20 fl oz)</td><td class=\"num\">473.176 ml</td><td class=\"num\">568.261 ml</td></tr>"
              "<tr><td>Gallon (8 pints)</td><td class=\"num\">3.785 l</td><td class=\"num\">4.546 l</td></tr>"
              "</tbody></table>",
              "<p>The difference exists because the two fluid ounces were defined against "
              "different gallons, and they have never been reconciled. Recipes are the only place "
              "it bites; a pint of beer is a different matter and has its own legislation.</p>"])


# ----------------------------------------------------------------- general units
def build_general_pages() -> None:
    hub = f"""
<h1>Unit conversions</h1>
<p class="lede">Length, mass and volume — converted from the definitions, with the arithmetic
shown.</p>
{ad_slot("top")}
<p>Unlike baking measurements, these conversions are exact. An inch has been 2.54&nbsp;cm since
the international yard and pound agreement of 1959, so a mile is 1.609344&nbsp;km with no
rounding at all. Any rounding on these pages is in the display only.</p>
{units_widget("length", "Length")}
{units_widget("mass", "Mass")}
{units_widget("volume", "Volume")}
<h2>Individual conversions</h2>
<div class="grid">
{"".join(f'<a href="/convert/{slug}/">{e(slug.replace("-", " ").title())}<span>{e(frm)} → {e(to)}</span></a>' for slug, frm, to, _cat, _note in GENERAL_CONVERSIONS)}
</div>
{ad_slot("bottom")}
"""
    page("/convert/", "Unit conversions — length, mass and volume",
         "Exact unit conversions for length, mass and volume, with live converters and full "
         "reference tables.", hub, priority=0.8)

    for slug, frm, to, cat, note in GENERAL_CONVERSIONS:
        table = UNIT_SYSTEMS[cat]["units"]
        f_factor, t_factor = table[frm], table[to]
        # 1 <from> = k <to>
        k = f_factor / t_factor
        base_rows = "".join(
            f'<tr><td>{e(name)}</td><td class="num">{fmt(f_factor / t_factor, 6)}</td></tr>'
            for name, f_factor2 in table.items())
        value_rows = "".join(
            f'<tr><td class="num">{fmt(v, 4)}</td><td class="num">{fmt(v * k, 6)}</td></tr>'
            for v in (0.1, 0.5, 1, 2, 5, 10, 25, 50, 100, 500, 1000))
        crumb = [("Conversions", "/convert/"), (f"{frm} to {to}", f"/convert/{slug}/")]
        body = f"""
<h1>{e(frm)} to {e(to)}</h1>
<p class="lede">One {e(frm.split('(')[0].strip())} is <strong>{fmt(k, 6)}</strong>
{e(to.split('(')[0].strip())}.</p>
{ad_slot("top")}
{converter(k, frm, to, "Type in either box; the other updates as you type.",
           from_decimals=4, to_decimals=6, default_from="1")}
<h2>Why this conversion is exact</h2>
<p>{e(note)}</p>
<h2>Reference values</h2>
<table><thead><tr><th class="num">{e(frm)}</th><th class="num">{e(to)}</th></tr></thead>
<tbody>{value_rows}</tbody></table>
{ad_slot("mid")}
<h2>Every {e(cat)} unit in {e(to)}</h2>
<table><thead><tr><th>Unit</th><th class="num">In {e(to.split('(')[0].strip())}</th></tr></thead>
<tbody>{base_rows}</tbody></table>
{ad_slot("bottom")}
"""
        page(f"/convert/{slug}/", f"{frm} to {to} — exact converter",
             f"Convert {frm} to {to}: one unit is {fmt(k, 6)}. Live converter and reference "
             f"tables, converted from the definitions.", body, crumb=crumb,
             jsonld=[breadcrumb_ld(crumb)], priority=0.6)


# ----------------------------------------------------------------- tools
def build_scaler() -> None:
    body = f"""
<h1>Recipe scaler</h1>
<p class="lede">Halve, double or triple a recipe — with the quantities in grams, so the
arithmetic stays honest.</p>
{ad_slot("top")}
<form class="scale card">
<p><label for="factor">Multiply by</label>
<input id="factor" name="factor" type="text" inputmode="decimal" value="1.5" style="width:6em"></p>
<table><thead><tr><th>Ingredient</th><th class="num">Original</th><th class="num">Scaled</th></tr></thead>
<tbody>
<tr><td>Plain flour</td><td class="num">250 g</td>
    <td class="num"><input data-base="250" value="250" style="width:6em" inputmode="decimal"></td></tr>
<tr><td>Granulated sugar</td><td class="num">200 g</td>
    <td class="num"><input data-base="200" value="200" style="width:6em" inputmode="decimal"></td></tr>
<tr><td>Butter</td><td class="num">175 g</td>
    <td class="num"><input data-base="175" value="175" style="width:6em" inputmode="decimal"></td></tr>
<tr><td>Eggs</td><td class="num">3</td>
    <td class="num"><input data-base="3" value="3" style="width:6em" inputmode="decimal"></td></tr>
</tbody></table>
<p class="hint">Edit the original column to match your recipe; the scaled column follows the
multiplier.</p>
</form>
<h2>Scaling rules that matter more than the arithmetic</h2>
<p>Multiplying everything by 1.5 is easy; what goes wrong is the tin, the time and the raising
agents. A deeper tin needs a longer, cooler bake, so drop the oven by 10&nbsp;°C and add ten
minutes. Baking powder and soda do not scale perfectly — use about 90% of the arithmetic
figure when doubling, or the crumb turns soapy. Salt, spices and vanilla can be scaled at
100%; eggs are best rounded to the nearest whole egg and the liquid adjusted to compensate.</p>
"""
    page("/recipe-scaler/", "Recipe scaler — halve or double a recipe",
         "Scale a recipe up or down, with the quantities in grams and the rules that stop a "
         "doubled cake going wrong.", body, priority=0.6)


# ----------------------------------------------------------------- static pages
def build_static_pages() -> None:
    page("/about/", "About this site",
         "What this site is for, who maintains it, and the convention it uses for weights.",
         f"""
<h1>About</h1>
<p class="lede">A small reference site for the measurements that trip up cooking — built
because most conversion pages ignore the one thing that matters: how the cup was filled.</p>
<p>Every weight here is a per-ingredient figure with a stated measuring convention, not a
single generic "cup equals 240&nbsp;ml". Every unit conversion is computed from its
definition. Where a number is a kitchen convention rather than a definition — gas marks, fan
oven offsets — it says so on the page.</p>
<p>The site is entirely static. No accounts, no tracking scripts, no advertising scripts by
default, and no cookies set by us.</p>
<p><a href="/methodology/">How these numbers are sourced</a> explains the references and the
rounding.</p>
""", priority=0.4)

    page("/methodology/", "How these numbers are sourced",
         "The references behind the ingredient weights, the definitions behind the unit "
         "conversions, and what is a kitchen convention rather than a fact.",
         f"""
<h1>How these numbers are sourced</h1>
<h2>Ingredient weights</h2>
<p>Per-cup weights come from <a href="https://www.kingarthurbaking.com/learn/ingredient-weight-chart"
rel="nofollow">King Arthur Baking's ingredient weight chart</a>, which is unusual among
published charts in stating the measuring convention it used: a US customary cup of
236.588&nbsp;ml, spooned and levelled. Where the chart gives a weight for a tablespoon or half
cup, the per-cup figure on this site is that value scaled — the arithmetic is noted in the
source file.</p>
<p>These figures are typical, not absolute. Brands mill differently, humidity changes the
weight of flour, and packing a cup changes it more than either. Treat any figure here as a good
centre, not a specification.</p>
<h2>Unit conversions</h2>
<p>Length, mass and volume convert from definitions fixed by the international yard and pound
agreement of 1959 and the metric system: 1 inch = 25.4&nbsp;mm, 1 pound = 0.45359237&nbsp;kg,
1 mile = 1609.344&nbsp;m, 1 US cup = 236.5882365&nbsp;ml. The arithmetic is done in the
generator, so the same figure appears identically wherever it appears.</p>
<h2>Oven temperatures</h2>
<p>Celsius and Fahrenheit convert by formula and are exact. Fan oven offsets (20&nbsp;°C) and
gas marks are British kitchen conventions, not physics — your oven's thermostat is probably
less accurate than either.</p>
<h2>Corrections</h2>
<p>If a number here is wrong, it is a defect and worth reporting:
<a href="/contact/">contact</a>.</p>
""", priority=0.4)

    page("/privacy/", "Privacy",
         "What this site collects (nothing), cookies, and what will change if advertising is "
         "enabled.",
         f"""
<h1>Privacy</h1>
<p>This site is static. It sets no cookies, runs no analytics and loads no third-party
scripts. Our server keeps ordinary access logs — IP address, page, timestamp — as every web
server does, for security and capacity.</p>
<h2>If advertising is added</h2>
<p>Google AdSense requires a certified consent management platform for visitors in the UK, the
EEA and Switzerland, which will ask for consent before any personalised advertising runs. This
page will be updated, with the specific partners listed, before the first ad appears.</p>
<h2>Contact</h2>
<p>Questions about this notice: <a href="/contact/">contact us</a>.</p>
""", priority=0.3)

    page("/contact/", "Contact",
         "How to reach the person who maintains this site.",
         """
<h1>Contact</h1>
<p>Corrections, questions and complaints are all welcome — particularly corrections, since the
point of the site is that the numbers are right.</p>
<p>Email: <strong>hello@daveys.xyz</strong></p>
""", priority=0.3)

    page("/404.html", "Page not found",
         "That page does not exist.", """
<h1>Page not found</h1>
<p class="lede">That page does not exist — but the converters certainly do.</p>
<ul>
<li><a href="/cups-to-grams/">Cups to grams, by ingredient</a></li>
<li><a href="/oven-temperatures/">Oven temperature conversions</a></li>
<li><a href="/pan-sizes/">Pan sizes</a></li>
<li><a href="/volume/">Volume measures</a></li>
<li><a href="/convert/">Unit conversions</a></li>
</ul>
""", priority=0.1)


# ----------------------------------------------------------------- files
def build_files() -> None:
    (OUT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf8")

    urls = "".join(
        f"  <url><loc>{url(p['path'])}</loc><lastmod>{TODAY}</lastmod>"
        f"<priority>{p['priority']:.1f}</priority></url>\n" for p in PAGES)
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}</urlset>\n", encoding="utf8")

    if ADSENSE_CLIENT:
        ads = f"google.com, {ADSENSE_CLIENT.replace('ca-', '')}, DIRECT, f08c47fec0942fa0\n"
    else:
        ads = ("# ads.txt placeholder — replace when the AdSense publisher ID is known:\n"
               "# google.com, pub-0000000000000000, DIRECT, f08c47fec0942fa0\n")
    (OUT / "ads.txt").write_text(ads, encoding="utf8")

    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    for asset in ("style.css", "app.js", "consent.js"):
        src = ROOT / "assets" / asset
        if src.exists():
            shutil.copy2(src, OUT / "assets" / asset)


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    build_home()
    build_ingredient_pages()
    build_oven_pages()
    build_pan_pages()
    build_volume_pages()
    build_general_pages()
    build_scaler()
    build_static_pages()
    build_files()
    print(f"built {len(PAGES)} pages into {OUT.relative_to(ROOT)}")
    print(f"AdSense: {'live as ' + ADSENSE_CLIENT if ADSENSE_CLIENT else 'placeholder (inert ad slots only)'}")


if __name__ == "__main__":
    main()
