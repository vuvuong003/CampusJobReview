from .views import MyTokenObtainPairView, RegisterView
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path

# This class defines the URL rouring. Defines the endpoints that the application will respond
# to, linking them to appropriate views that handle requests and return
# responses.

urlpatterns = [
    # This endpoint when accessed triggers the  MyTokenObtainPairView.as_view to handle the request/
    # Deals with user authentication and returns JWT token upon successful login.
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # This endpoint is for refreshing a JWT token by handling the login for refreshing an
    # expired token and returning a new one.
    path('token/refresh/', TokenRefreshView.as_view, name='token_refresh'),
    # Handles registration, allowing new users to sign up and create an account
    path('register/', RegisterView.as_view(), name='register')

]
# allows our AP to respond to requests with different formats.
urlpatterns = format_suffix_patterns(urlpatterns)
