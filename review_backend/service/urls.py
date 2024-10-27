from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ReviewsViewSet
from .views import VacanciesViewSet
router = DefaultRouter()
router.register(r'reviews', ReviewsViewSet)
router.register(r'vacancies', VacanciesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]



