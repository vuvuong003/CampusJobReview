"""
Serializer for the Reviews model.

This serializer handles the validation and serialization of Review instances.
"""
from rest_framework import serializers
from .models import Reviews, Vacancies

# Disable the "too-few-public-methods" warning for this class
# since it typically require only one or no methods.

# pylint: disable=R0903
class ReviewsSerializer(serializers.ModelSerializer):
    """
    Serializer for the Reviews model.

    This class provides validation and serialization for Review instances.
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
            'review': {'required': True},  # Enforces non-null constraint
            'rating': {'required': True},  # Enforces non-null constraint
            'locations': {'required': False},  # Optional field
            'job_description': {'required': False},  # Optional field,
            'reviewed_by': {'required': False},  # Optional field,
        }

    def validate(self, attrs):
        """
        Validate the incoming attributes for a Review instance.

        Args:
            attrs (dict): The attributes to validate.

        Raises:
            serializers.ValidationError: If validation fails.
        """
        # Add custom validation logic here if needed
        if attrs['rating'] < 1 or attrs['rating'] > 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5.")
        if not attrs['review']:
            raise serializers.ValidationError("Review cannot be empty.")
        # Add more validation as needed
        return attrs

# Disable the "too-few-public-methods" warning for this class
# since it typically require only one or no methods.

# pylint: disable=R0903
class VacanciesSerializer(serializers.ModelSerializer):
    """
    Serializer for the Vacancies model.

    This serializer handles the validation and serialization of Vacancy instances.
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
        """
        Validate the incoming attributes for a Vacancy instance.

        Args:
            attrs (dict): The attributes to validate.

        Raises:
            serializers.ValidationError: If validation fails.
        """
        # Add custom validation logic here if needed
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
