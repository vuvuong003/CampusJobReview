"""
URL configuration for the 'service' application.

This module defines the URL patterns for the 'service' app, including
the endpoints and their associated views. It uses Django's URL routing
system to map URLs to specific views in the application.
"""
# Import suffix patterns for URL formatting
# from rest_framework.urlpatterns import format_suffix_patterns  # pylint: disable=E0401
# from django.urls import path

from django.urls import include, path # Import 'include' and 'path' for URL configuration
from rest_framework.routers import DefaultRouter # Import DefaultRouter for automated URL routing
# Local application imports
from .views import ReviewsViewSet, VacanciesViewSet, ReviewsView, CommentViewSet

# Initialize the default router for automatically handling URLs for viewsets
router = DefaultRouter()
router.register(r'reviews', ReviewsViewSet) # Register 'reviews' endpoint with ReviewsViewSet
router.register(r'vacancies', VacanciesViewSet) # Register 'vacancies' endpoint with
# VacanciesViewSet

# Define URL patterns for the service application
urlpatterns = [
    path('', include(router.urls)), # Include router-generated URLs for registered viewsets
    path('comments/<int:id>/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comments'),
    path('comments/<int:id>/<int:comment_id>/', CommentViewSet.as_view({'delete': 'destroy'}), name='delete-comment'),
    path('all_reviews/', ReviewsView.as_view(), name='get-reviews')
]
