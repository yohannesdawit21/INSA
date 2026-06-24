"""Views for the Josephus visualizer.

`index`  -> renders the interactive page.
`solve`  -> a tiny JSON API the frontend calls to get the elimination order.
"""
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .josephus import josephus_sequence

# Keep the inputs sane so the animation stays readable and the server safe.
MAX_PEOPLE = 200


@require_GET
def index(request):
    return render(request, "visualizer/index.html")


@require_GET
def solve(request):
    """Compute the elimination order for given n and k.

    Query params:
        n -> number of people
        k -> elimination interval
    """
    try:
        n = int(request.GET.get("n", ""))
        k = int(request.GET.get("k", ""))
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "n and k must be whole numbers."}, status=400
        )

    if n < 1 or k < 1:
        return JsonResponse(
            {"error": "n and k must both be at least 1."}, status=400
        )

    if n > MAX_PEOPLE:
        return JsonResponse(
            {"error": f"Please use {MAX_PEOPLE} people or fewer."}, status=400
        )

    result = josephus_sequence(n, k)
    return JsonResponse({"n": n, "k": k, **result})
