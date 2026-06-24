"""
Arabic (decimal) -> Ge'ez numeral conversion.

Same algorithm as the original challenge-01.py CLI script, plus two extras
the animated frontend needs:

  * per-glyph metadata  -> so each symbol can show its value on hover
  * a place-value breakdown -> so the conversion can be explained step by step

Ge'ez numerals (Ethiopic):
    ፩..፱  = 1..9          (ones)
    ፲..፺  = 10..90        (tens)
    ፻     = 100           (hundred)
    ፼     = 10,000        (ten-thousand)
There is no symbol for zero.
"""

ONES = ["", "፩", "፪", "፫", "፬", "፭", "፮", "፯", "፰", "፱"]
TENS = ["", "፲", "፳", "፴", "፵", "፶", "፷", "፸", "፹", "፺"]

# char -> (numeric value, short label) used for hover tooltips on the frontend.
GLYPH_INFO = {}
for _i in range(1, 10):
    GLYPH_INFO[ONES[_i]] = (_i, str(_i))
    GLYPH_INFO[TENS[_i]] = (_i * 10, str(_i * 10))
GLYPH_INFO["፻"] = (100, "100")
GLYPH_INFO["፼"] = (10000, "10,000")


def under_100(n):
    """Ge'ez for a number 0..99 (tens glyph + ones glyph)."""
    return TENS[n // 10] + ONES[n % 10]


def arabic_to_geez(n):
    """Convert a non-negative integer to its Ge'ez numeral string."""
    result = ""

    if n >= 10000:
        part = n // 10000
        if part > 1:
            result += arabic_to_geez(part)
        result += "፼"
        n %= 10000

    if n >= 100:
        part = n // 100
        if part > 1:
            result += under_100(part)
        result += "፻"
        n %= 100

    if n > 0:
        result += under_100(n)

    return result


def _breakdown(n):
    """Split n into the place groups Ge'ez uses, largest first.

    Returns a list of dicts the frontend animates as breakdown rows.
    """
    groups = []

    if n >= 10000:
        part = n // 10000
        groups.append({
            "place": "Ten-thousands",
            "symbol": "፼",
            "count": part,
            "subtotal": part * 10000,
            "geez": (arabic_to_geez(part) if part > 1 else "") + "፼",
        })
        n %= 10000

    if n >= 100:
        part = n // 100
        groups.append({
            "place": "Hundreds",
            "symbol": "፻",
            "count": part,
            "subtotal": part * 100,
            "geez": (under_100(part) if part > 1 else "") + "፻",
        })
        n %= 100

    if n > 0:
        groups.append({
            "place": "Units (1–99)",
            "symbol": "",
            "count": n,
            "subtotal": n,
            "geez": under_100(n),
        })

    return groups


def convert(n):
    """Full conversion payload for the API.

    Returns a dict with the Ge'ez string, per-glyph metadata, and the
    place-value breakdown.
    """
    geez = arabic_to_geez(n)
    glyphs = []
    for ch in geez:
        value, label = GLYPH_INFO.get(ch, (None, ch))
        glyphs.append({"ch": ch, "value": value, "label": label})

    return {
        "n": n,
        "geez": geez,
        "glyphs": glyphs,
        "groups": _breakdown(n),
    }
