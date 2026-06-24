"""WSGI entry point for the Josephus visualizer project."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "josephus_site.settings")

application = get_wsgi_application()
