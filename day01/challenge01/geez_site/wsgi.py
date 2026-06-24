"""WSGI entry point for the Ge'ez converter project."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "geez_site.settings")

application = get_wsgi_application()
