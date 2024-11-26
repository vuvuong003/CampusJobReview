"""
Module for defining custom serializers for user authentication and registration.

This module contains serializers that handle the generation of JWT tokens for
user authentication and the registration of new users, including custom
validation and user attribute management.
"""
from rest_framework import serializers  # pylint: disable=E0401
from rest_framework.validators import UniqueValidator  # pylint: disable=E0401
from rest_framework.exceptions import ValidationError  # Use this for consistency
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer  # pylint: disable=E0401

# Import for enforcing strong passwords
from django.contrib.auth.password_validation import validate_password  # pylint: disable=E0401
# Get user model dynamically
from django.contrib.auth import get_user_model

# Third-party imports
# from rest_framework import serializers  # pylint: disable=E0401
# from rest_framework.exceptions import ValidationError
# from rest_framework.validators import UniqueValidator  # pylint: disable=E0401
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer  # pylint: disable=E0401

User = get_user_model() # Retrieve the User model
# pylint: disable=R0903

# pylint: disable=W0223
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer for obtaining a JSON Web Token (JWT) for user authentication.

    This serializer extends the default TokenObtainPairSerializer to add
    custom claims to the JWT, such as the username.

    Methods:
        get_token(user): Generates a JWT for the given user, adding custom claims.
    """
    @classmethod
    def get_token(cls, user):
        """
        Generate a JWT for the specified user.

        Args:
            cls: The class itself (used for class methods).
            user: The user instance for whom the token is being generated.

        Raises:
            ValidationError: If the user instance is None.

        Returns:
            token: An instance of the token with added custom claims.
        """

        if user is None:
            raise ValidationError("User does not exist.")
        if not user.is_verified:
            raise ValidationError("Email is not verified.")

        token = super(MyTokenObtainPairSerializer, cls).get_token(user) # Generate token
        token["username"] = user.username  # Add custom claim for username
        token["is_verified"] = user.is_verified
        return token

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering new users.

    This serializer handles the validation and creation of new user accounts,
    enforcing password validation and ensuring required fields are filled.

    Attributes:
        username (str): The username of the user, required for registration.
        password (str): The password for the user account, validated for security.

    Methods:
        create(validated_data): Creates a new user instance with the validated data.
    """
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())] # Ensures unique usernames
    )

    email = serializers.EmailField(
        required=True,
    )

    password = serializers.CharField(
        write_only=True, # Password will not be returned in serialized output
        # password is required field
        required=True, # Field is required for user creation
        validators=[validate_password],
        style={'input_type': 'password'}# Enforce strong password requirements
    )


    # called when creating an user.
    def create(self, validated_data):
        """
        Create a new user instance with the validated data.

        Args:
            validated_data (dict): The validated data containing username and password.

        Returns:
            User: The created user instance.
        """
        # Create user with username
        user = User.objects.create(username=validated_data["username"],
                                   email=validated_data['email'],
                                   is_verified=False)
        user.is_active = True # Set user to active state
        user.is_admin = True # Grant admin privileges
        user.set_password(validated_data["password"]) # Securely hash the password
        user.save() # Save the user instance to the database

        return user

    # defines how the serializer interacts with the model
    class Meta:
        """
        Metadata options for the RegisterSerializer, defining how it interacts with the User model.

        Attributes:
            model (Model): The model associated with the serializer.
            fields (list): Fields included in the serialized output.
        """
        model = User # Link serializer to the User model
        fields = ["username", "password", "email"] # Specify fields to include in output

class ProfileSerializer(serializers.ModelSerializer):
    """
        Serializer for user's profile info.
    """
    class Meta:
        """
        Metadata for the ProfileSerializer, defining how it interacts with the User model.

        Attributes:
            model (Model): The mnodel associated with the Serializer.
            fields (list): Fields included in the serialized output.
            read_only_fields (list): Fields which cannot be modified.
        """
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio']
        read_only_fields = ['username', 'email']
