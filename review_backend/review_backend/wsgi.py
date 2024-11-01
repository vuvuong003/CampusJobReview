"""
WSGI config for review_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os # Import the os module to interact with the operating system
# Import Django's WSGI application handler
from django.core.wsgi import get_wsgi_application  # pylint: disable=E0401
# Set the default Django settings module for the 'review_backend' project.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "review_backend.settings")
# Get the WSGI application for the project.
# This callable is used by WSGI servers to forward requests to Django.
application = get_wsgi_application()
