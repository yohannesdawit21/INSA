# Challenge 01 — Code Logic (Arabic → Ge'ez Converter)

This document explains **how the code works**, end to end: the conversion
algorithm, the Django backend, and the JavaScript that animates it.

> High-level overview lives in [README.md](README.md).

---

## 1. The Ge'ez numeral system (background)

Ge'ez (Ethiopic) numerals have **no zero** and use these symbols:

| Symbol | Value | | Symbol | Value |
|:------:|:-----:|---|:------:|:-----:|
| ፩–፱ | 1–9 (ones) | | ፻ | 100 |
| ፲–፺ | 10–90 (tens) | | ፼ | 10,000 |

A number is built by **place groups**: ten-thousands (፼), hundreds (፻), and the
remaining 1–99 written as a tens-glyph + ones-glyph. For example
**1234 = (12 × ፻) + 34 → ፲፪፻፴፬**.

---

## 2. The algorithm — `converter/geez.py`

### Helper tables

```python
ONES = ["", "፩","፪","፫","፬","፭","፮","፯","፰","፱"]   # index == digit
TENS = ["", "፲","፳","፴","፵","፶","፷","፸","፹","፺"]   # index == tens digit
```

The empty string at index `0` is the trick that makes "no zero" work
automatically: `ONES[0]` and `TENS[0]` contribute nothing.

### `under_100(n)` — numbers 0–99

```python
def under_100(n):
    return TENS[n // 10] + ONES[n % 10]
```

`n // 10` is the tens digit, `n % 10` is the ones digit. Concatenate their
glyphs. E.g. `34` → `TENS[3] + ONES[4]` → `፴` + `፬` → `፴፬`.

### `arabic_to_geez(n)` — the full number

This is the original challenge logic, unchanged in spirit:

```python
def arabic_to_geez(n):
    result = ""
    if n >= 10000:                       # ten-thousands group
        part = n // 10000
        if part > 1:
            result += arabic_to_geez(part)   # recurse for the count
        result += "፼"
        n %= 10000
    if n >= 100:                         # hundreds group
        part = n // 100
        if part > 1:
            result += under_100(part)
        result += "፻"
        n %= 100
    if n > 0:                            # remaining 1–99
        result += under_100(n)
    return result
```

Read it as three slices of the number, largest first:

- **Ten-thousands**: how many ፼? If more than one, write the count *before* the
  ፼ symbol. The count itself can exceed 99, so it **recurses** through
  `arabic_to_geez`. Then drop those with `n %= 10000`.
- **Hundreds**: how many ፻? Write the count (0–99) with `under_100`, then ፻.
  `if part > 1` skips writing "1" — `100` is just `፻`, not `፩፻`.
- **Units**: whatever is left (1–99) via `under_100`.

### `GLYPH_INFO` — metadata for the UI

```python
GLYPH_INFO[ONES[i]] = (i, str(i))        # ፬ -> (4, "4")
GLYPH_INFO[TENS[i]] = (i*10, str(i*10))  # ፴ -> (30, "30")
GLYPH_INFO["፻"] = (100, "100")
GLYPH_INFO["፼"] = (10000, "10,000")
```

A lookup from each character to its **value + label**, so the frontend can show
"፴ = 30" when you hover a glyph.

### `_breakdown(n)` — the place-value explanation

Mirrors `arabic_to_geez`, but instead of building a string it returns a list of
**groups** the UI animates as rows:

```python
{"place": "Hundreds", "symbol": "፻", "count": 12,
 "subtotal": 1200, "geez": "፲፪፻"}
```

Each group records *what place it is*, *how many*, *its running value*, and
*its Ge'ez text*.

### `convert(n)` — the API payload

Ties it together: the final string, a per-character glyph list (with values from
`GLYPH_INFO`), and the breakdown.

```python
{
  "n": 1234,
  "geez": "፲፪፻፴፬",
  "glyphs": [{"ch": "፲", "value": 10, "label": "10"}, ...],
  "groups": [{"place": "Hundreds", ...}, {"place": "Units (1–99)", ...}]
}
```

---

## 3. The backend — `converter/views.py`

| URL | View | Returns |
|-----|------|---------|
| `/` | `index` | the HTML page |
| `/api/convert?n=` | `convert` | the JSON payload above |

`convert` validates before computing:

- not a whole number → HTTP 400,
- negative → 400 ("Ge'ez numerals are for positive numbers"),
- above `MAX_NUMBER` (100,000,000) → 400 (keeps glyph strings readable),
- **`n == 0`** → handled specially: Ge'ez has no zero, so it returns an empty
  result plus a `note` instead of a blank string.

Otherwise it returns `convert(n)`. No database, no state — pure computation per
request.

---

## 4. The animation — `templates/converter/index.html`

All client-side JS (wrapped in `{% verbatim %}` so Django ignores the braces).

### `convert()` — fetch + render

Debounced on every keystroke (280 ms) and bound to the button / Enter / chips:

```js
const res = await fetch("/api/convert?n=" + encodeURIComponent(n));
const data = await res.json();
if (!res.ok) throw new Error(data.error);
render(data);
```

### `render(data)` — the glyphs and breakdown

1. **Glyphs**: for each character it makes a `<span class="glyph">`, tags hundreds
   and ten-thousands with the `.mult` class (green), sets a hover tooltip from
   the metadata, and **staggers the entrance**:
   ```js
   el.dataset.tip = g.label + " = " + g.value;
   el.style.animationDelay = (i * 0.09) + "s";   // each glyph a beat later
   ```
   The `glyphIn` CSS keyframe does the 3D flip-and-pop; the delay makes them
   appear left-to-right.
2. **Breakdown rows**: one `.row` per group, also staggered, showing
   `count × value = subtotal` and that group's Ge'ez.
3. **Total**: confirms the groups sum back to the original number.

### The reference chart — `buildRef()`

Loops `ONES` and `TENS` (plus ፻ and ፼) to render a hoverable grid of every
symbol with its value — built once on page load.

### Where the CSS does the work

JS only sets text, classes, and `animationDelay`. The motion is CSS:
- `@keyframes glyphIn` — the staggered flip-in of each glyph,
- `@keyframes slideIn` — breakdown rows sliding in,
- `.glyph:hover` lift + `::after` tooltip, `.ref:hover` enlarge.

---

## 5. Putting it together

```
Browser ── GET /api/convert?n=1234 ──▶ Django (views.convert)
                                          │ geez.convert(1234)
Browser ◀── {geez:"፲፪፻፴፬",             ──┘
             glyphs:[...], groups:[...]} ── JSON
   │
   └─ JS pops in each glyph (staggered) and slides in the breakdown rows.
```

The Python decides **what the number becomes**; the JavaScript decides **how it
appears**.
