"""
URL configuration for the 'service' application.

This module defines the URL patterns for the 'service' app, including
the endpoints and their associated views. It uses Django's URL routing
system to map URLs to specific views in the application.
"""
from rest_framework.urlpatterns import format_suffix_patterns #pylint: disable=E0401
# from django.urls import path

urlpatterns = []
urlpatterns = format_suffix_patterns(urlpatterns)
