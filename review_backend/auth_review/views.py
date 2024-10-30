from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer

from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth import get_user_model

# This class is responsible for handling essential functionality for user
# registration and authentication.

# allows for interaction with user objects
User = get_user_model()

# This class manages user registration and ensures that a username is
# unique before creating a new user.


class RegisterView(APIView):
    # This view can be accessed by anyone without authentication
    permission_classes = [AllowAny]

    def post(self, request, format=None):
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
    # Allows token endpoint access to anyone
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer

    # get requests not allowed for this endpoint
    def get(self, requests, format=None):
        return Response({"msg": "Get not allowed"})

    def post(self, requests, format=None):
        r = super().post(requests, format)
        # successful authentication then retreive the username from the request and search for user's index in the
        # database.
        # If the token generation fails, return the original response
        if r.status_code == 200:

            return Response(
                {
                    "data": {
                        "val": True,
                        "tokens": r.data,
                    }
                },
                status=status.HTTP_200_OK,
            )
        return r
