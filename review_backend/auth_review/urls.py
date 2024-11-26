"""
Module for defining URL routing for the 'auth_review' application.

This module contains the URL patterns that map to specific views
handling user authentication, registration, and token management.
It leverages Django REST Framework's URL routing capabilities to
create clean and manageable endpoints for the API.
"""
# Import format pattern utility to enable different response formats (e.g., JSON, HTML)
from rest_framework.urlpatterns import format_suffix_patterns  # pylint: disable=E0401
# Import view for refreshing JWT tokens
from rest_framework_simplejwt.views import TokenRefreshView  # pylint: disable=E0401
# Import path function to define URL patterns
from django.urls import path  # pylint: disable=E0401
# Import custom views for obtaining JWT tokens and registering users
from .views import MyTokenObtainPairView, RegisterView
from .views import  VerifyEmailView, SendOtpView, UpdatePasswordView
from .views import ProfileView


# Define URL routing for the auth_review application.
urlpatterns = [
    # This endpoint when accessed triggers the  MyTokenObtainPairView.as_view to handle the request/
    # Deals with user authentication and returns JWT token upon successful login.
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    # Endpoint for refreshing a JWT token. Routes to TokenRefreshView,
    # which manages refreshing an expired token to provide a new one.
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Endpoint for user registration. Routes to RegisterView, allowing
    # new users to sign up and create an account in the system.
    path("register/", RegisterView.as_view(), name="register"),

    path("verify-email/<str:uidb64>/<str:token>/", VerifyEmailView.as_view(), name="verify_email"),

    path("profile/", ProfileView.as_view(), name="profile"),

    path("send-otp/", SendOtpView.as_view(), name="send_otp"),

    path("update-password/", UpdatePasswordView.as_view(), name="update_password")
]
# Enable the API to respond to different formats by applying format suffix patterns
urlpatterns = format_suffix_patterns(urlpatterns)
