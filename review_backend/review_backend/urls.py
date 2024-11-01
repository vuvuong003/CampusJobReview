"""
URL configuration for review_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Import the Django admin module
from django.contrib import admin  # pylint: disable=E0401
# Import path and include functions for URL routing
from django.urls import path, include  # pylint: disable=E0401

# Define the URL patterns for the project, mapping each path to the appropriate view or app
urlpatterns = [
    # Admin site path, accessible at '/admin/' in the URL
    path("admin/", admin.site.urls),
    # Routes requests starting with 'auth/' to the URL configurations defined in 'auth_review.urls'
    path("auth/", include("auth_review.urls")),
    # Routes requests starting with 'service/' to the URL configurations defined in 'service.urls'
    path("service/", include("service.urls")),
]
