from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

# This class defines a custom token serializer and a registration serializer for user authentication 
# and registration. The customization allows for additional claims in the JWT, enforce password validating during
# user creating, and ensuring security with proper handling of data.


User = get_user_model()

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
 
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        #add custom claims to the token. adds username claim to the token which allows
        # client to receive the username when a token is generated
        token['username'] = user.username
        return token


# responsible for serializing user registration data
class RegisterSerializer(serializers.ModelSerializer):

    # serializer field for the username, which is required for registration
    username = serializers.CharField(
        required = True,
    )

    # serializer field for the password.
    password = serializers.CharField(
        # password will not be included in the serialized output
        write_only=True,
        # password is required field
        required=True,
        # password is validated to ensure it meets security claims
        validators = [validate_password]
    )

    # called when creating an user. 
    def create(self, validated_data):
        
        # creates a user object with the provided username
        user = User.objects.create(
            username = validated_data["username"]
        )
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
        model = User
        fields = ['username', 'password']