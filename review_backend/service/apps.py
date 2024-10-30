"""
Django application configuration for the 'service' app.

This module contains the configuration for the 'service' application, which
is part of the Django project. It sets up the application name and default
primary key field type.
"""
from django.apps import AppConfig #pylint: disable=E0401

# Disable the "too-few-public-methods" warning for this class
# since AppConfig subclasses typically require only one or no methods.

#pylint: disable=R0903
class ServiceConfig(AppConfig):
    """
    Django application configuration for the 'service' app.

    This class is responsible for configuring the 'service' application within
    the Django project. It sets the default auto field type and provides
    metadata for the app.

    Attributes:
        default_auto_field (str): The type of field to use for auto-created
        primary keys. Default is 'BigAutoField'.
        name (str): The name of the application, used for referring to the
        app in other parts of Django.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "service"
