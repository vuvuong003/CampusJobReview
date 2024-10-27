from rest_framework import viewsets
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


class VacanciesViewSet(viewsets.ModelViewSet):
    queryset = Vacancies.objects.all()  # Get all vacancies
    serializer_class = VacanciesSerializer  # Use the VacanciesSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  # Get data from the request
        if serializer.is_valid():  # Validate the data
            serializer.save()  # Save the valid data to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return created response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return error response