"""Top-level URL routing — everything lives in the converter app."""
from django.urls import include, path

urlpatterns = [
    path("", include("converter.urls")),
]
