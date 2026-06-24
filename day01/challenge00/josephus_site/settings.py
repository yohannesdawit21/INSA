"""
Django settings for the Josephus visualizer project.

Kept intentionally minimal: no database is needed because the whole
challenge runs in memory. This is a single-app demo project.
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# For a local demo this is fine. Do not ship this key to production.
SECRET_KEY = "django-insecure-josephus-demo-key-change-me"

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "visualizer",
]

MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "josephus_site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [],
        },
    },
]

WSGI_APPLICATION = "josephus_site.wsgi.application"

# No database is required for this project.
DATABASES = {}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
