"""
Module for configuring the 'auth_review' application within the Django project.

This module contains the configuration for the 'auth_review' application,
which is responsible for handling user authentication, registration, and
review management. It sets the default primary key field type and provides
metadata for the app.
"""
# Import Django's base AppConfig for app configuration settings
from django.apps import AppConfig  # pylint: disable=E0401

# Disable the "too-few-public-methods" warning for this class
# since AppConfig subclasses typically require only one or no methods.

# pylint: disable=R0903


class AuthReviewConfig(AppConfig):
    """Django application configuration for the 'auth_review' app.

    This class is responsible for configuring the 'auth_review' application
    within the Django project. It sets the default auto field type and
    provides metadata for the app.

    Attributes:
        default_auto_field (str): The type of field to use for auto-created
            primary keys. Default is 'BigAutoField'.
        name (str): The name of the application, used for referring to the
            app in other parts of Django.
    """
    default_auto_field = "django.db.models.BigAutoField" # Set BigAutoField
    # as default for primary key fields
    name = "auth_review" # Define the name of the app as 'auth_review'
