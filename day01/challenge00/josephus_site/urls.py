"""Top-level URL routing — everything lives in the visualizer app."""
from django.urls import include, path

urlpatterns = [
    path("", include("visualizer.urls")),
]
