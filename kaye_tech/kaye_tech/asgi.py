"""
ASGI config for kaye_tech project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kaye_tech.settings")

application = get_asgi_application()
daphne - p 2901 kaye_tech.asgi: application
