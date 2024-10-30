"""
URL configuration for the 'service' application.

This module defines the URL patterns for the 'service' app, including
the endpoints and their associated views. It uses Django's URL routing
system to map URLs to specific views in the application.
"""
from rest_framework.urlpatterns import format_suffix_patterns  # pylint: disable=E0401
# from django.urls import path

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ReviewsViewSet
from .views import VacanciesViewSet
from .views import FilterReviewsView

router = DefaultRouter()
router.register(r'reviews', ReviewsViewSet)
router.register(r'vacancies', VacanciesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('filter/', FilterReviewsView.as_view(), name='filter-reviews'),
]
