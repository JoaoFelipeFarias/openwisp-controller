"""
WSGI config for pfsense_captive project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if os.environ['PFSENSE_CAPTIVE_ENVIRONMENT'] == 'DEV':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")



application = get_wsgi_application()
