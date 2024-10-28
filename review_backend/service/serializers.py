from rest_framework import serializers
from .models import Reviews, Vacancies


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = '__all__'  # This will include all fields from the Reviews model
        extra_kwargs = {
            'department': {'required': True},  # Enforces non-null constraint
            'job_title': {'required': True},  # Enforces non-null constraint
            'hourly_pay': {'required': True},  # Enforces non-null constraint
            'review': {'required': True},  # Enforces non-null constraint
            'rating': {'required': True},  # Enforces non-null constraint
            'locations': {'required': False},  # Optional field
            'job_description': {'required': False},  # Optional field
        }

    def validate(self, attrs):
        # Add custom validation logic here if needed
        if attrs['rating'] < 1 or attrs['rating'] > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        if not attrs['review']:
            raise serializers.ValidationError("Review cannot be empty.")
        # Add more validation as needed
        return attrs

class VacanciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancies
        fields = '__all__'  # This will include all fields from the Vacancies model

    def validate(self, attrs):
        # Add custom validation logic here if needed
        if not attrs['jobTitle']:
            raise serializers.ValidationError("Job title cannot be empty.")
        if not attrs['jobDescription']:
            raise serializers.ValidationError("Job description cannot be empty.")
        if attrs['maxHoursAllowed'] <= 0:
            raise serializers.ValidationError("Max hours allowed must be greater than 0.")
        # Add more validation as needed
        return attrs