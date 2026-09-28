#!/usr/bin/env python3
"""Validate the generated site: internal links, JSON-LD, required head tags."""
import json, re, sys
from pathlib import Path

PUB = Path(__file__).resolve().parent.parent / "public"
pages = sorted(PUB.rglob("*.html"))
problems = {"links": [], "jsonld": [], "head": []}

existing = set()
for p in PUB.rglob("*"):
    if p.is_file():
        existing.add("/" + str(p.relative_to(PUB)))

def target_exists(href: str) -> bool:
    href = href.split("#")[0].split("?")[0]
    if not href.startswith("/"):
        return True
    if href in existing:
        return True
    if href.endswith("/") and (href + "index.html") in existing:
        return True
    if (href + "/index.html") in existing or href + ".html" in existing:
        return True
    return False

link_count = 0
for page in pages:
    text = page.read_text(encoding="utf8")
    rel = "/" + str(page.relative_to(PUB))
    for m in re.finditer(r'(?:href|src)="(/[^"]*)"', text):
        link_count += 1
        if not target_exists(m.group(1)):
            problems["links"].append(f"{rel} -> {m.group(1)}")
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', text, re.S):
        try:
            json.loads(m.group(1))
        except Exception as exc:
            problems["jsonld"].append(f"{rel}: {exc}")
    for tag in ('<title>', 'name="description"', 'rel="canonical"'):
        if tag not in text:
            problems["head"].append(f"{rel}: missing {tag}")
    if text.count("<h1") != 1:
        problems["head"].append(f"{rel}: {text.count('<h1')} h1 tags")

print(f"pages: {len(pages)}  internal hrefs/src checked: {link_count}")
for kind, items in problems.items():
    print(f"\n{kind}: {len(items)} problem(s)")
    for item in items[:15]:
        print("   ", item)
sys.exit(1 if any(problems.values()) else 0)
