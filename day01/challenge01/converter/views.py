"""Views for the Ge'ez numeral converter.

`index`    -> renders the interactive page.
`convert`  -> a tiny JSON API the frontend calls to convert a number.
"""
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .geez import convert as convert_number

# Cap the input so glyph strings stay readable on screen.
MAX_NUMBER = 100_000_000


@require_GET
def index(request):
    return render(request, "converter/index.html")


@require_GET
def convert(request):
    """Convert a decimal number to Ge'ez.

    Query param:
        n -> the number to convert (0 .. MAX_NUMBER)
    """
    raw = request.GET.get("n", "")
    try:
        n = int(raw)
    except (TypeError, ValueError):
        return JsonResponse({"error": "Please enter a whole number."}, status=400)

    if n < 0:
        return JsonResponse(
            {"error": "Ge'ez numerals are for positive numbers."}, status=400
        )

    if n > MAX_NUMBER:
        return JsonResponse(
            {"error": f"Please use a number up to {MAX_NUMBER:,}."}, status=400
        )

    if n == 0:
        # Ge'ez has no zero — answer explicitly instead of an empty string.
        return JsonResponse(
            {"n": 0, "geez": "", "glyphs": [], "groups": [],
             "note": "Ge'ez has no symbol for zero."}
        )

    return JsonResponse(convert_number(n))
