"""
Views for the 'service' application.

This module contains the view functions and classes that handle
HTTP requests and responses for the 'service' app. These views
interact with the models and serializers to implement the business
logic and provide the appropriate responses to the client.
"""
# from django.shortcuts import render
from rest_framework import viewsets # Import viewsets for creating API views
from rest_framework import generics # Import generics for generic API views
from rest_framework.response import Response # Import Response for HTTP responses
from rest_framework import status # Import status codes for HTTP responses
from rest_framework.permissions import IsAuthenticated # Import authentication permissions
from .models import Reviews # Import Reviews model for review-related views
from .serializers import ReviewsSerializer # Import serializer for Reviews

from .models import Vacancies # Import Vacancies model for vacancy-related views
from .serializers import VacanciesSerializer # Import serializer for Vacancies

# pylint: disable=R0901
class ReviewsViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing Reviews.

    This viewset provides standard actions for creating, retrieving,
    updating, and deleting Review instances. It restricts access to
    authenticated users and handles the associated business logic.
    """
    permission_classes = (IsAuthenticated,) # Restrict access to authenticated users only
    # pylint: disable=E1101
    queryset = Reviews.objects.all()   # Get all Review objects from the database
    serializer_class = ReviewsSerializer  # Specify the serializer for data conversion

    # pylint: disable=W0107,W0221
    def retrieve(self, request, pk=None):
        "testing retrieve without affecting functionality. this is solely test"
        pass
    # pylint: disable=W0613,R0903
    def create(self, request, *args, **kwargs):
        """
        Create a new Review instance.

        This method overrides the default create method to include 
        the user who created the review.

        Args:
            request (Request): The HTTP request containing the review data.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A response containing the created review data or errors.
        """
        user = request.user # Get the user making the request
        request.data['reviewed_by'] = user.username # Add username to the review data
        serializer = self.get_serializer(data=request.data)  # Serialize incoming data
        if serializer.is_valid():  # Check if the serialized data is valid
            # print(serializer.data)
            serializer.save()  # Save data to the database if valid
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED) # Return success response with serialized data
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)  # Return error response if data is invalid


class ReviewsView(generics.ListAPIView):
    """
    A view for fetching all Reviews.
    """
    # permission_classes = (IsAuthenticated)
    serializer_class = ReviewsSerializer # Use the Reviews serializer for data representation

    def get_queryset(self):
        """
        Retrieve a list of all Review instances.

        Returns:
            QuerySet: A queryset of all Review instances.
        """
        # pylint: disable=E1101
        queryset = Reviews.objects.all() # get all reviews
        return queryset



class VacanciesViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing Vacancies.

    This viewset provides standard actions for creating, retrieving,
    updating, and deleting Vacancy instances. It manages vacancy data
    and handles the associated business logic.
    """
    # pylint: disable=E1101
    queryset = Vacancies.objects.all()  # Get all Vacancy objects from the database
    serializer_class = VacanciesSerializer   # Specify the serializer for data conversion
    # pylint: disable=W0613
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
            data=request.data)   # Serialize incoming data
        if serializer.is_valid():  # Check if the serialized data is valid
            serializer.save()  # Save data to the database if valid
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED)  # Return success response with serialized data
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)   # Return error response if data is invalid
