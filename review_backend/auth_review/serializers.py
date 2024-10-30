"""
Module for defining custom serializers for user authentication and registration.

This module contains serializers that handle the generation of JWT tokens for
user authentication and the registration of new users, including custom
validation and user attribute management.
"""
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer  # pylint: disable=E0401
from rest_framework import serializers  # pylint: disable=E0401
# from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model  # pylint: disable=E0401
from django.contrib.auth.password_validation import validate_password  # pylint: disable=E0401

User = get_user_model()
# This class defines a custom token serializer and a registration serializer for user authentication
# and registration. The customization allows for additional claims in the JWT,
# enforce password validating during user creating, and ensuring security with proper handling of
# data.

# Disable the "too-few-public-methods" warning for this class
# since AppConfig subclasses typically require only one or no methods.

# pylint: disable=R0903


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer for obtaining a JSON Web Token (JWT) for user authentication.

        This serializer extends the default TokenObtainPairSerializer to add
        custom claims to the JWT, such as the username.

    Methods:
        get_token(user): Generates a JWT for the given user, adding custom claims.
    """
    @classmethod
    def get_token(cls, user):
        """Generate a JWT for the specified user.

        Args:
            cls: The class itself (used for class methods).
            user: The user instance for whom the token is being generated.

        Returns:
            An instance of the token with added custom claims.
        """
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # add custom claims to the token. adds username claim to the token which allows
        # client to receive the username when a token is generated
        token["username"] = user.username
        return token


# responsible for serializing user registration data
# Disable the "too-few-public-methods" warning for this class
# since AppConfig subclasses typically require only one or no methods.
class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for registering new users.

    This serializer handles the validation and creation of new user accounts,
    enforcing password validation and ensuring required fields are filled.

    Attributes:
        username (str): The username of the user, required for registration.
        password (str): The password for the user account, validated for security.

    Methods:
        create(validated_data): Creates a new user instance with the validated data.
    """
    # serializer field for the username, which is required for registration
    username = serializers.CharField(
        required=True,
    )

    # serializer field for the password.
    password = serializers.CharField(
        # password will not be included in the serialized output
        write_only=True,
        # password is required field
        required=True,
        # password is validated to ensure it meets security claims
        validators=[validate_password],
    )

    # called when creating an user.
    def create(self, validated_data):
        """Create a new user instance with the validated data.

        Args:
            validated_data (dict): The validated data containing username and password.

        Returns:
            User: The created user instance.
        """
        # creates a user object with the provided username
        user = User.objects.create(username=validated_data["username"])
        # user can log in
        user.is_active = True
        # grant admin privileges
        user.is_admin = True
        # hash the password securely
        user.set_password(validated_data["password"])
        user.save()

        return user

    # defines how the serializer interacts with the model
    class Meta:
        """
        This class provides metadata options for the RegisterSerializer,
        defining how the serializer interacts with the User model.

        Attributes:
            model (Model): The model that the serializer is associated with.
            fields (list): A list of field names that should be included in the serialized output.
        """
        model = User
        fields = ["username", "password"]
