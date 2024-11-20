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
#from rest_framework.exceptions import PermissionDenied # Import Response for HTTP responses
from rest_framework import status # Import status codes for HTTP responses
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated # Import authentication permissions
from .models import Reviews # Import Reviews model for review-related views
from .serializers import ReviewsSerializer # Import serializer for Reviews

from .models import Vacancies # Import Vacancies model for vacancy-related views
from .serializers import VacanciesSerializer # Import serializer for Vacancies

from .models import Comment # Import Vacancies model for comment-related views
from .serializers import CommentSerializer # Import serializer for Comment

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


class FilterReviewsView(generics.ListAPIView):
    """
    A view for filtering Reviews.

    This view provides the ability to filter reviews based on various
    query parameters such as department, locations, job title, and rating.
    """
    # permission_classes = (IsAuthenticated)
    serializer_class = ReviewsSerializer # Use the Reviews serializer for data representation

    def get_queryset(self):
        """
        Retrieve a filtered list of Review instances.

        This method applies filters based on query parameters provided 
        in the request.

        Returns:
            QuerySet: A queryset of filtered Review instances.
        """
        # pylint: disable=E1101
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
        print(list(queryset)[0].reviewed_by)
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

class CommentViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing Comments related to Reviews.

    This viewset provides standard actions for creating, retrieving,
    updating, and deleting Comment instances. Comments are associated
    with specific reviews and users.
    """
    permission_classes = [IsAuthenticated] # Restrict access to authenticated users only
    queryset = Comment.objects.all() # Get all Comment objects from the database
    serializer_class = CommentSerializer # Specify the serializer for data conversion
    
    def get_queryset(self):
        """
        Retrieve comments related to a specific review.

        This method retrieves comments filtered by the review ID provided
        in the URL.

        Args:
            request (Request): The HTTP request containing the review ID.

        Returns:
            QuerySet: A queryset of filtered Comment instances.
        """
        review_id = self.kwargs.get('id')  # Get review ID from URL
        return Comment.objects.filter(review_id=review_id)  # Filter comments by review_id
    
    def perform_create(self, serializer):
        """
        Create a new Comment instance.

        This method overrides the default create method to assign the 
        appropriate review and user to the comment before saving it.

        Args:
            serializer (Serializer): The serializer instance for the comment data.

        Returns:
            None: The comment is saved automatically by the serializer.
        """
        review_id = self.kwargs.get('id') # Extract the review_id from the URL
        review = get_object_or_404(Reviews, id=review_id)  # Get the review object
        user = self.request.user #Get the current user
        serializer.save(review=review, user=user)  # Assign the review to the comment
    
    def destroy(self, request, *args, **kwargs):
        id = kwargs.get('id')  # Extract the review ID from the URL
        comment_id = kwargs.get('comment_id')  # Extract the comment ID from the URL
        
        try:
            # Ensure the comment exists with the given review ID
            comment = Comment.objects.get(id=comment_id, review_id=id)
        except Comment.DoesNotExist:
            return Response({'detail': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the user is authorized to delete the comment
        # if comment.user != request.user:
        #     raise PermissionDenied("You are not allowed to delete this comment.")
        
        comment.delete()
        return Response({'detail': 'Comment deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)