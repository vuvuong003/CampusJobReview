"""
This module contains serializers for the Reviews and Vacancies models, enabling
validation and serialization of data for RESTful
APIs in a Django application.

Components:
- **ReviewsSerializer**: Serializes the Reviews model, enforcing required fields
and custom validation rules for attributes such as rating and review content.
- **VacanciesSerializer**: Serializes the Vacancies model, ensuring that critical
fields like job title and job description are provided, and validates constraints
on the maximum hours allowed.

Functions:
- **ReviewsSerializer.validate**: Custom validation for Reviews, ensuring the rating
is between 1 and 5 and that the review field is not empty.
- **VacanciesSerializer.validate**: Custom validation for Vacancies, checking that
job title and job description are not empty and that the maximum hours allowed is greater than zero.
"""
from rest_framework import serializers  # Import Django REST framework serializers
from .models import Reviews, Vacancies, Comment # Import models to create serializers for



# pylint: disable=R0903
class ReviewsSerializer(serializers.ModelSerializer):
    """Serializer for the Reviews model.

    This serializer handles the conversion of Reviews model instances to JSON format
    and vice versa, ensuring data consistency and validation before saving.

    Meta Attributes:
        model (Reviews): Specifies the Reviews model for serialization.
        fields (str): Includes all model fields.
        extra_kwargs (dict): Specifies required fields to enforce non-null constraints.
    """
    class Meta:
        """
        Meta options for the ReviewsSerializer.

        Attributes:
            model: The model associated with this serializer (Reviews).
            fields: A list of fields to include in the serialization.
            extra_kwargs: Additional constraints for specific fields, such as
                          requiring certain fields to be present.
        """
        model = Reviews
        fields = '__all__'  # This will include all fields from the Reviews model
        extra_kwargs = {
            'department': {'required': True},  # Enforces non-null constraint
            'job_title': {'required': True},  # Enforces non-null constraint
            'hourly_pay': {'required': True},  # Enforces non-null constraint
            'review': {'required': False},  # Enforces non-null constraint
            'rating': {'required': True},  # Enforces non-null constraint
            'locations': {'required': False},  # Optional field
            'job_description': {'required': False},  # Optional field,
            'reviewed_by': {'required': False},  # Optional field,
            'recommendation': {'required': False},
        }

    def validate(self, attrs):
        """Custom validation for Reviews model data.

        Ensures that `rating` is within the valid range (1-5) and that `review` content
        is provided if required. 

        Args:
            attrs (dict): Attributes being validated.

        Raises:
            serializers.ValidationError: If validation constraints are violated.

        Returns:
            dict: Validated attributes.
        """
        # Add custom validation logic here if needed
        if attrs['rating'] < 1 or attrs['rating'] > 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5.")
        if not attrs['review']:
            raise serializers.ValidationError("Review cannot be empty.")
        return attrs

# Disable the "too-few-public-methods" warning for this class
# since it typically require only one or no methods.

# pylint: disable=R0903
class VacanciesSerializer(serializers.ModelSerializer):
    """Serializer for the Vacancies model.

    This serializer converts Vacancies model data to JSON format for API
    responses and performs data validation for attributes before saving.

    Meta Attributes:
        model (Vacancies): Specifies the Vacancies model for serialization.
        fields (str): Includes all fields of the Vacancies model.
    """
    class Meta:
        """
        Meta options for the VacanciesSerializer.

        Attributes:
            model: The model associated with this serializer (Vacancies).
            fields: A list of fields to include in the serialization.
        """
        model = Vacancies
        fields = '__all__'  # This will include all fields from the Vacancies model

    def validate(self, attrs):
        """Custom validation for Vacancies model data.

        Checks that critical fields like job title and job description are not
        empty and that `maxHoursAllowed` is greater than zero.

        Args:
            attrs (dict): Attributes to be validated.

        Raises:
            serializers.ValidationError: If any validation constraint is violated.

        Returns:
            dict: Validated attributes.
        """
        if not attrs['jobTitle']:
            raise serializers.ValidationError("Job title cannot be empty.")
        if not attrs['jobDescription']:
            raise serializers.ValidationError(
                "Job description cannot be empty.")
        if attrs['maxHoursAllowed'] <= 0:
            raise serializers.ValidationError(
                "Max hours allowed must be greater than 0.")
        # Add more validation as needed
        return attrs
    
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'review', 'user', 'text', 'created_at']
        extra_kwargs = {
            'text': {'required': True},
            'review': {'read_only': True},
            'user': {'read_only': True},
        }

    def validate(self, data):
        if not data.get('text'):
            raise serializers.ValidationError("Text is required.")
        return data
