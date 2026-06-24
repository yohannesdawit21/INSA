# Arabic → Ge'ez — Interactive Django Converter

An animated web app that converts ordinary (Arabic) numbers into **Ge'ez**
(Ethiopic) numerals — the same algorithm as the original `challenge- 01.py`
CLI script, wrapped in a beautiful, motion-filled UI.

## Features

- 🔢 Type any number and watch each Ge'ez glyph **pop in** one by one
- 🖱️ Hover any glyph to see its numeric value
- 🧮 Live **place-value breakdown** (ten-thousands ፼ / hundreds ፻ / units) that slides in
- 📖 Built-in **reference chart** of every Ge'ez numeral symbol (hover to enlarge)
- 🎲 Example chips + random button, warm Ethiopian-inspired theme, animated background
- 🔌 Tiny JSON API (`/api/convert?n=`) powered by the original algorithm

## Run it

```bash
# from this folder (day01/challenge01/)
python3 manage.py runserver
```

Then open **http://127.0.0.1:8000/** in your browser.

> Requires Django (`pip install Django`). Already installed in the `base` env.
> Tip: if challenge00 is already running on port 8000, start this one on
> another port: `python3 manage.py runserver 8001`.

## Project layout

```
challenge01/
├── manage.py                     # Django entry point
├── geez_site/                    # project config (settings, urls, wsgi)
├── converter/                    # the app
│   ├── geez.py                   # the algorithm + per-glyph metadata + breakdown
│   ├── views.py                  # page view + JSON API
│   ├── urls.py
│   └── templates/converter/
│       └── index.html            # the entire animated UI (HTML/CSS/JS)
└── challenge- 01.py              # the original CLI version
```

## Ge'ez numerals at a glance

| Symbol | Value | | Symbol | Value |
|:------:|:-----:|---|:------:|:-----:|
| ፩–፱ | 1–9 (ones) | | ፻ | 100 |
| ፲–፺ | 10–90 (tens) | | ፼ | 10,000 |

There is **no symbol for zero**, so the app says so explicitly when you enter 0.

> 📖 For a line-by-line walkthrough of the algorithm, backend, and animation
> code, see [LOGIC.md](LOGIC.md).

## How it fits together

1. The browser calls `GET /api/convert?n=1234`.
2. `views.convert` validates the number and runs `geez.convert(n)`.
3. The API returns the Ge'ez string, per-glyph metadata, and the breakdown.
4. The frontend animates the glyphs and breakdown rows.

Example: **1234** → `፲፪፻፴፬` = (12 × 100) + 34.
