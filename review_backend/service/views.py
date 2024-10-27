from django.shortcuts import render
from rest_framework import viewsets
from .models import Reviews, Vacancies
from .serializers import ReviewsSerializer, VacanciesSerializer
# Create your views here.


class ReviewsViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing review instances.
    """
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer


class VacanciesViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing vacancy instances.
    """
    queryset = Vacancies.objects.all()
    serializer_class = VacanciesSerializer
