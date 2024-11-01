"""
URL configuration for the 'service' application.

This module defines the URL patterns for the 'service' app, including
the endpoints and their associated views. It uses Django's URL routing
system to map URLs to specific views in the application.
"""
# Import suffix patterns for URL formatting
from rest_framework.urlpatterns import format_suffix_patterns  # pylint: disable=E0401
# from django.urls import path

from django.urls import include, path # Import 'include' and 'path' for URL configuration
from rest_framework.routers import DefaultRouter # Import DefaultRouter for automated URL routing
from .views import ReviewsViewSet # Import ReviewsViewSet for handling review-related views
from .views import VacanciesViewSet # Import VacanciesViewSet for handling vacancy-related views
from .views import FilterReviewsView # Import FilterReviewsView for handling filtered review views

# Initialize the default router for automatically handling URLs for viewsets
router = DefaultRouter()
router.register(r'reviews', ReviewsViewSet) # Register 'reviews' endpoint with ReviewsViewSet
router.register(r'vacancies', VacanciesViewSet) # Register 'vacancies' endpoint with VacanciesViewSet

# Define URL patterns for the service application
urlpatterns = [
    path('', include(router.urls)), # Include router-generated URLs for registered viewsets
    path('filter/', FilterReviewsView.as_view(), name='filter-reviews'), # Define 'filter/' path for filtered reviews view
]
