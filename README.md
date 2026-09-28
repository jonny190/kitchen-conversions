# Kitchen Conversions

A small, fast reference site for cooking measurements — cups to grams by ingredient,
oven temperatures across Celsius, Fahrenheit, fan and gas mark, pan sizes, and volume
equivalents between US, UK and metric measures.

Built as a static site: `generator/build.py` writes `public/`, which is copied into an
nginx image and deployed to Coolify. No runtime, no database, no build step on the server,
no client-side tracking.

## Build

```bash
python3 generator/build.py          # writes ./public
python3 -m http.server -d public 8000   # preview at http://localhost:8000
```

`generator/build.py` is stdlib-only. Content lives beside it:

- `content/ingredients.py` — ingredient weights, per-cup grams, notes and tips
- `content/tables.py` — oven temperatures, pan sizes, volume measures, general units

## AdSense placeholder

Nothing advertises yet, and adding it is deliberately a one-line change:

1. `generator/build.py` → set `ADSENSE_CLIENT = "ca-pub-XXXXXXXXXXXXXXXX"`.
   Until then the head carries a commented-out `google-adsense-account` meta tag and every
   page renders an inert `<div class="adslot">` marker, so placement is already decided.
2. `public/ads.txt` is generated with a placeholder line — replace the publisher ID.
3. Consent: UK and EEA traffic requires a **Google-certified consent management platform**
   before any personalised ad may serve. `assets/consent.js` is an empty placeholder wired
   into every page; plug the CMP snippet in there.

## Deployment

Coolify builds the `Dockerfile` and serves it behind Traefik at `https://kitchen.daveys.xyz`.
The DNS record is a plain A record to the origin; no tunnel is involved.

## Editing

Change content, run the build, commit. Every page — tables, FAQ, JSON-LD, sitemap — is
generated, so numbers never drift between pages.
