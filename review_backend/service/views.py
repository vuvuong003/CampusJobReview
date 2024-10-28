from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Reviews
from .serializers import ReviewsSerializer

from .models import Vacancies
from .serializers import VacanciesSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()  # Get all reviews
    serializer_class = ReviewsSerializer  # Use the ReviewsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  # Get data from the request
        if serializer.is_valid():  # Validate the data
            serializer.save()  # Save the valid data to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return created response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return error response
    
class FilterReviewsView(generics.ListAPIView):
    serializer_class = ReviewsSerializer

    def get_queryset(self):
        queryset = Reviews.objects.all()
        department = self.request.query_params.get('department', None)
        locations = self.request.query_params.get('locations', None)
        job_title = self.request.query_params.get('job_title', None)
        min_rating = self.request.query_params.get('min_rating', None)
        max_rating = self.request.query_params.get('max_rating', None)

        if department:
            queryset = queryset.filter(department__icontains=department)
        if locations:
            queryset = queryset.filter(locations__icontains=locations)
        if job_title:
            queryset = queryset.filter(job_title__icontains=job_title)
        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)
        if max_rating:
            queryset = queryset.filter(rating__lte=max_rating)

        return queryset    


class VacanciesViewSet(viewsets.ModelViewSet):
    queryset = Vacancies.objects.all()  # Get all vacancies
    serializer_class = VacanciesSerializer  # Use the VacanciesSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  # Get data from the request
        if serializer.is_valid():  # Validate the data
            serializer.save()  # Save the valid data to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return created response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return error response