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


class ReviewsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,) # Restrict access to authenticated users only
    queryset = Reviews.objects.all()   # Get all Review objects from the database
    serializer_class = ReviewsSerializer  # Specify the serializer for data conversion

    def create(self, request, *args, **kwargs):
        user = request.user # Get the user making the request
        request.data['reviewed_by'] = user.username # Add username to the review data
        serializer = self.get_serializer(data=request.data)  # Serialize incoming data
        if serializer.is_valid():  # Check if the serialized data is valid
            serializer.save()  # Save data to the database if valid
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED) # Return success response with serialized data
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)  # Return error response if data is invalid 


class FilterReviewsView(generics.ListAPIView):
    # permission_classes = (IsAuthenticated)
    serializer_class = ReviewsSerializer # Use the Reviews serializer for data representation

    def get_queryset(self):
        queryset = Reviews.objects.all() # Start with all reviews
        department = self.request.query_params.get('department', None) # Get 'department' param
        locations = self.request.query_params.get('locations', None) # Get 'locations' param
        job_title = self.request.query_params.get('job_title', None) # Get 'job_title' param
        min_rating = self.request.query_params.get('min_rating', None) # Get 'min_rating' param
        max_rating = self.request.query_params.get('max_rating', None) # Get 'max_rating' param
        # Apply filters if parameters are provided
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
    queryset = Vacancies.objects.all()  # Get all Vacancy objects from the database
    serializer_class = VacanciesSerializer   # Specify the serializer for data conversion

    def create(self, request, *args, **kwargs):
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
