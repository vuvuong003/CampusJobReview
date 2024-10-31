"""
Views for the 'service' application.

This module contains the view functions and classes that handle
HTTP requests and responses for the 'service' app. These views
interact with the models and serializers to implement the business
logic and provide the appropriate responses to the client.
"""
# from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Reviews
from .serializers import ReviewsSerializer

from .models import Vacancies
from .serializers import VacanciesSerializer
#pylint
class ReviewsViewSet(viewsets.ModelViewSet):
    """
    A view set for handling Reviews.

    This view set provides actions for listing, creating, retrieving,
    updating, and deleting reviews. It is restricted to authenticated
    users for creating reviews.
    """
    permission_classes = (IsAuthenticated,)
    queryset = Reviews.objects.all()  # Get all reviews
    serializer_class = ReviewsSerializer  # Use the ReviewsSerializer
    # pylint: disable=W0613,R0903
    def create(self, request, *args, **kwargs):
        """
        Create a new Review instance.

        This method overrides the default create method to add the
        'reviewed_by' field automatically from the authenticated user.

        Args:
            request (Request): The HTTP request containing the review data.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A response containing the created review data or errors.
        """
        user = request.user
        request.data['reviewed_by'] = user.username
        serializer = self.get_serializer(data=request.data)  # Get data from the request
        if serializer.is_valid():  # Validate the data
            serializer.save()  # Save the valid data to the database
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED)  # Return created response
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)  # Return error response

# pylint: disable=R0903
class FilterReviewsView(generics.ListAPIView):
    """
    A view for filtering Reviews.

    This view provides the ability to filter reviews based on various
    query parameters such as department, locations, job title, and rating.
    """
    # permission_classes = (IsAuthenticated)
    serializer_class = ReviewsSerializer

    def get_queryset(self):
        """
        Retrieve and filter the queryset of Reviews.

        This method allows filtering by department, locations, job title,
        and rating range through query parameters.

        Returns:
            QuerySet: The filtered queryset of reviews.
        """
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

# pylint: disable=R0903
class VacanciesViewSet(viewsets.ModelViewSet):
    """
    A view set for handling Vacancies.

    This view set provides actions for listing, creating, retrieving,
    updating, and deleting vacancies.
    """
    queryset = Vacancies.objects.all()  # Get all vacancies
    serializer_class = VacanciesSerializer  # Use the VacanciesSerializer
    # pylint: disable=W0613,R0903
    def create(self, request, *args, **kwargs):
        """
        Create a new Vacancy instance.

        This method overrides the default create method to handle the
        creation of a vacancy.

        Args:
            request (Request): The HTTP request containing the vacancy data.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A response containing the created vacancy data or errors.
        """
        serializer = self.get_serializer(
            data=request.data)  # Get data from the request
        if serializer.is_valid():  # Validate the data
            serializer.save()  # Save the valid data to the database
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED)  # Return created response
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)  # Return error response
