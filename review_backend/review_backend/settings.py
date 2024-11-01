"""
Django settings for review_backend project.

Generated by 'django-admin startproject' using Django 5.1.2.

This file contains the configuration settings for the Django project,
including application settings, database configurations, middleware,
URL routing, and other essential components.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os # Import the os module to interact with the operating system
from pathlib import Path # Import Path class for easy path manipulations
from datetime import timedelta # Import timedelta for token lifetime settings
# Import to load environment variables from .env file
from dotenv import load_dotenv  # pylint: disable=E0401


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-@-jt)j-cog1i!sh%pos55&)(6$^)2v+ym#*%j*^x^e(a3(+(x#"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False # Disable debug mode for production

ALLOWED_HOSTS = ['localhost', '127.0.0.1'] # Define allowed hosts for development

ALLOWED_HOSTS = ['*'] # Allow all hosts (not recommended for production)


# Application definition

INSTALLED_APPS = [
    # Default Django applications
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party applications
    "rest_framework", # Django REST Framework for building APIs
    "auth_review", # Custom application for authentication review
    "service", # Custom application for additional services
    "corsheaders", # CORS headers management
    "rest_framework_simplejwt",  # Simple JWT for token management
]
# Set the custom user model for authentication
AUTH_USER_MODEL = "auth_review.Client"
# Django REST Framework configuration
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication", # Use JWT for authentication
    ],
}
# Configuration for Simple JWT token settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=10), # Set access token lifetime
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1), # Set refresh token lifetime
    "ROTATE_REFRESH_TOKENS": False, # Disable refresh token rotation
    "BLACKLIST_AFTER_ROTATION": True, # Enable blacklist after token rotation
    "UPDATE_LAST_LOGIN": False, # Disable updating last login
    "ALGORITHM": "HS256", # Set the algorithm for token encoding
    "SIGNING_KEY": SECRET_KEY, # Use the secret key for signing tokens
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",), # Define accepted authorization header types
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION", # Set the authorization header name
    'USER_ID_FIELD': 'username', # Use username as the user ID field
    "USER_ID_CLAIM": "user_id", # Claim name for user ID
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",), # Define token classes
    "TOKEN_TYPE_CLAIM": "token_type", # Claim name for token type
    "JTI_CLAIM": "jti",  # Claim name for JWT ID
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp", # Claim for sliding token refresh expiration
    "SLIDING_TOKEN_LIFETIME": timedelta(days=10), # Set sliding token lifetime
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1), # Set sliding token refresh lifetime
}

# Middleware settings for processing requests
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware", # Security middleware
    "django.contrib.sessions.middleware.SessionMiddleware", # Session management
    "django.middleware.common.CommonMiddleware", # Common middleware
    "django.middleware.csrf.CsrfViewMiddleware", # CSRF protection
    "django.contrib.auth.middleware.AuthenticationMiddleware", # Authentication middleware
    "django.contrib.messages.middleware.MessageMiddleware", # Message framework
    "django.middleware.clickjacking.XFrameOptionsMiddleware", # Clickjacking protection
    "corsheaders.middleware.CorsMiddleware", # CORS middleware for handling cross-origin requests
]

CORS_ORIGIN_ALLOW_ALL = True # Allow all origins (not recommended for production)
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
] # Specify allowed headers for CORS
CORS_ALLOW_CREDENTIALS = False
# URL configuration for the project
ROOT_URLCONF = "review_backend.urls"
# Template settings
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates", # Set the template engine
        "DIRS": [], # Specify directories for custom templates
        "APP_DIRS": True, # Enable loading templates from app directories
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug", # Enable debugging context
                "django.template.context_processors.request", # Request context
                "django.contrib.auth.context_processors.auth", # Authentication context
                "django.contrib.messages.context_processors.messages", # Messages context
            ],
        },
    },
]

WSGI_APPLICATION = "review_backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
load_dotenv()
DATABASES = {
    "default": {
        "ENGINE": "djongo",
        "NAME": os.getenv("DB_NAME"),
        "CLIENT": {
            # 'host': "mongodb+srv://"+os.getenv('DB_USERNAME')+":"
            # +os.getenv("DB_PASSWORD")+"@cluster0.ohnr0.mongodb.net/"
            "host": "mongodb+srv://"
            + os.getenv("DB_USERNAME")
            + ":"
            + os.getenv("DB_PASSWORD")
            + "@cluster0.falr3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
