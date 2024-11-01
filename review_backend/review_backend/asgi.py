"""
ASGI config for review_backend project.

This module configures the ASGI application for the review_backend project,
exposing the ASGI callable as a module-level variable named ``application``.
It is essential for asynchronous communication in the Django project,
enabling compatibility with ASGI-compliant servers.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""
# Import the os module to manage environment settings
import os
# Import Django's function to get the ASGI application
from django.core.asgi import get_asgi_application  # pylint: disable=E0401
# Set the default Django settings module for the ASGI application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "review_backend.settings")
# Create the ASGI application instance, enabling the application to
# handle asynchronous requests and making it available to ASGI servers
application = get_asgi_application()
