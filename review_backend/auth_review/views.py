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
from rest_framework.exceptions import MethodNotAllowed
from rest_framework import status  # pylint: disable=E0401
from rest_framework_simplejwt.views import TokenObtainPairView  # pylint: disable=E0401
# from django.shortcuts import render
from django.contrib.auth import get_user_model  # pylint: disable=E0401
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer
from rest_framework import status
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
        user = User.objects.filter(
            Q(username=request.data["username"]) | Q(email=request.data["email"])
            )
        
        if len(user) > 0:
            return Response(
                {"data": {"val": False, "detail": "Entered username or email exists"}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # if username is unique, the serializer is instantiated with the
        # request data.
        serializer = RegisterSerializer(data=request.data)
        # serializer checks if the provided data is valid
        if serializer.is_valid():
            try:
                user = serializer.save()
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                verification_link = f"{settings.FRONTEND_URL}/verify-email/{uid}/{token}/"
                
                message = Mail(
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to_emails=user.email,
                    subject="Verify your email",
                    html_content=f"Click <a href='{verification_link}'>{verification_link}</a> to verify your email."
                )

                try:
                    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                    sg.send(message)
                    return Response(
                    {"data": {"val": True, "detail": "Registration Successful. Please verify your email."}},
                    status=status.HTTP_200_OK,
                    )
                except Exception as e:
                    # Delete the user if email sending fails
                    user.delete()
                    return Response(
                        {"data": {"val": False, "detail": f"Registration failed: {str(e)}"}},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
            except Exception as e:
                return Response(
                    {"data": {"val": False, "detail": f"Registration failed: {str(e)}"}},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
                
        return Response(
            {"data": {"val": False, "detail": serializer.errors}},
            status=status.HTTP_400_BAD_REQUEST,
        )

class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            
            if user is not None and default_token_generator.check_token(user, token):
                user.is_verified = True
                user.save()
                return Response(
                    {"message": "Email verified successfully."}, 
                    status=status.HTTP_200_OK
                )
            return Response(
                {"message": "Invalid verification link."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            print(f"Verification error: {str(e)}")  # Add debugging
            return Response(
                {"message": f"Invalid user ID: {str(e)}"}, 
                status=status.HTTP_400_BAD_REQUEST
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
    # pylint: disable=W0613
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
        raise MethodNotAllowed("GET", detail={"msg": "Get not allowed"})



    # pylint: disable=W0221,W0237
    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=request.data.get('username'))
            if not user.is_verified:
                return Response(
                    {"detail": "Please verify your email before logging in."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except User.DoesNotExist:
            pass

        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return Response(
                {
                    "data": {
                        "val": True,
                        "tokens": response.data,
                    }
                },
                status=status.HTTP_200_OK,
            )
        return response
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get user Profile"""
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        """Update user Profile"""
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SendOtpView(APIView):
    def post(self, request):
        try:
            email = request.data.get("email")
            generatedOtp = request.data.get("generated_otp")

            user = User.objects.get(email=email)

            if user is None:
                response_data = {'message' : 'Entered email id does not exist'}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            else:
                # metadata of mail (sender, recipient, subject and content)
                message = Mail(
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to_emails=user.email,
                    subject="Reset your password",
                    html_content=f"Hi {user.username}, <br/><br/>Your OTP for resetting your password is <b>{generatedOtp}</b>. Please use it within the next 10 minutes."
                )

                # sending mail
                sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                sg.send(message)

                return Response(data={"otp": generatedOtp}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            response_data = {'message' : 'Entered email id does not exist'}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
class UpdatePasswordView(APIView):
    """
    Handles updating password for an existing user

    Args:
        request: The HTTP request.

    Returns:
        Response: A response object containing an error message.  
    """
    def post(self, request):
        try:
            user = User.objects.get(email=request.data.get("email"))

            password = request.data.get("password")

            try:
                validate_password(password, user)
            except ValidationError as e:
                return Response({"errors": e.message}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(password)
            user.save()

            return Response({"message": "Password updated successfully!"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(data={'message': f'{e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

