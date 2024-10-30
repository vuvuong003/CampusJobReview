"""
Module for handling user registration and authentication in the application.

This module contains views that facilitate user registration and
authentication processes. It includes functionalities for ensuring
unique usernames during registration and generating JSON Web Tokens (JWT)
for authenticated users. The views utilize Django REST Framework's
APIView and serializers for managing request and response data.
"""


# Create your views here.
from rest_framework.views import APIView  # pylint: disable=E0401
from rest_framework.permissions import AllowAny  # pylint: disable=E0401
from rest_framework.response import Response  # pylint: disable=E0401
from rest_framework import status  # pylint: disable=E0401
from rest_framework_simplejwt.views import TokenObtainPairView  # pylint: disable=E0401
# from django.shortcuts import render
from django.contrib.auth import get_user_model  # pylint: disable=E0401
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer

# This class is responsible for handling essential functionality for user
# registration and authentication.

# allows for interaction with user objects
User = get_user_model()

# This class manages user registration and ensures that a username is
# unique before creating a new user.
# Disable the "too-few-public-methods" warning for this class
# since AppConfig subclasses typically require only one or no methods.

# pylint: disable=R0903


class RegisterView(APIView):
    """
    View for user registration.

    This view allows new users to register by providing a unique username
    and a password. It checks if the username already exists in the database
    and validates the provided data using the RegisterSerializer. If successful,
    it creates a new user account.

    Permission:
        AllowAny: This view can be accessed by anyone without
        authentication.

    Methods:
        post(request, _type=None): Handles POST requests for user registration.
    """
    # This view can be accessed by anyone without authentication
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle user registration requests.

        This method checks if the username provided already exists in the
        database. If it does, it returns a 400 BAD REQUEST response. If the
        username is unique, it validates the data with the RegisterSerializer
        and creates a new user if valid.

        Args:
            request: The HTTP request containing the registration data.


        Returns:
            Response: A response object containing the registration status
            and message.
        """
        # checks if username provided already exists in the database then
        # return with an 400 BAD REQUEST
        user = User.objects.filter(username=request.data["username"])
        if len(user) > 0:
            return Response(
                {"data": {"val": False, "detail": "Username Exists"}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # if username is unique, the serializer is instantiated with the
        # request data.
        serializer = RegisterSerializer(data=request.data)
        # serializer checks if the provided data is valid
        if serializer.is_valid():
            serializer.save()
            # if valid a new user is created with a success response. If not,
            # then return a BAD REQUEST
            return Response(
                {"data": {"val": True, "detail": "Registration Successful"}},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"data": {"val": False, "detail": serializer.errors}},
            status=status.HTTP_400_BAD_REQUEST,
        )


# view to authenticate
# This class handles user authenticaion and generates JWTs, providing
# additional custom data in the response
class MyTokenObtainPairView(TokenObtainPairView):
    """
    View for user authentication and JWT token generation.

    This view allows users to authenticate using their username and
    password, generating a JWT token upon successful authentication.
    It provides additional information about the user in the response.

    Permission:
        AllowAny: This view can be accessed by anyone without
        authentication.

    Methods:
        get(request): Handles GET requests to the token endpoint.
        post(request): Handles POST requests for token generation.
    """
    # Allows token endpoint access to anyone
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer

    # get requests not allowed for this endpoint
    def get(self, request):
        """
        Handle GET requests to the token endpoint.

        This method returns a message indicating that GET requests are not
        allowed for this endpoint.

        Args:
            request: The HTTP request.

        Returns:
            Response: A response object containing an error message.
        """
        return Response({"msg": "Get not allowed"})

    def post(self, requests):
        """
        Handle user authentication requests.

        This method processes authentication requests and generates a JWT
        token if the provided credentials are valid. It retrieves the
        user's index in the database to include additional details in the
        response.

        Args:
            request: The HTTP request containing the authentication data.


        Returns:
            Response: A response object containing the authentication status,
            generated tokens, and user details.
        """
        r = super().post(requests)
        # successful authentication then retreive the username from the request and search for
        # user's index in the database.
        # If the token generation fails, return the original response
        if r.status_code == 200:
            tenant_username = requests.data["username"]
            all_users = User.objects.all()
            tenant_id = 0
            for i in all_users:
                if i.username == tenant_username:
                    break
                tenant_id += 1

            # client = User.objects.get(username=obj["username"])
            # obj["username"] = client.username

            return Response(
                {
                    "data": {
                        "val": True,
                        "tokens": r.data,
                        "details": {"tenant_id": tenant_id},
                    }
                },
                status=status.HTTP_200_OK,
            )
        return r
