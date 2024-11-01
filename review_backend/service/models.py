"""
Module for defining database models for the 'service' application.

This module contains the definitions of the database models used in the
service application, including the Reviews and Vacancies models.
These models represent the data structures for storing review and job
vacancy information in the database.
"""
# Import Djongo models to work with MongoDB
from djongo import models  # pylint: disable=E0401
from rest_framework.exceptions import ValidationError # Import ValidationError for custom validation logic

# from django.contrib.auth.models import AbstractUser

# pylint: disable=R0903


class Reviews(models.Model):
    """Model that stores information about submitted reviews.

    Attributes:
        id (AutoField): Unique identifier for each review.
        department (str): The department related to the job.
        locations (str): The location of the job.
        job_title (str): The title of the job.
        job_description (str): A description of the job.
        hourly_pay (str): The pay rate for the job.
        benefits (str): The benefits offered for the job.
        review (str): The text of the review.
        rating (int): The rating given by the reviewer.
        recommendation (int): Indicates whether the reviewer would recommend the job.
    """

    # Unique identifier for each review
    department = models.CharField(max_length=100, blank=False, null=False) # Department name
    locations = models.CharField(max_length=120, db_index=True, blank=True) # Job location
    job_title = models.CharField(max_length=64, db_index=True, null=False) # Job description
    job_description = models.CharField(max_length=120, db_index=True, blank=True, null=True) 
    hourly_pay = models.CharField(max_length=10, null=False, blank=False) # Pay rate as a string
    benefits = models.CharField(max_length=120, db_index=True, null=False, blank=True) # Job benefits
    review = models.CharField(max_length=120, db_index=True, null=True, blank=True) # Review text
    rating = models.IntegerField(null=False, blank=False) # Rating out of 5
    recommendation = models.IntegerField(null=True, blank=True) # Recommendation flag

    def clean(self):
        """Custom validation logic for the Reviews model.

        Validates that required fields are not null and that `rating` is within the valid range (1-5).
        Also ensures `hourly_pay` and `review` are strings.
        
        Raises:
            ValidationError: If any validation constraint is violated.
        """
        super().clean()
        if not self.department:
            raise ValidationError("Department cannot be null.")
        if not self.job_title:
            raise ValidationError("Job Title cannot be null.")
        if not self.hourly_pay:
            raise ValidationError("Hourly Pay cannot be null.")
        if self.rating is None:  # Check if rating is null
            raise ValidationError("Rating cannot be null.")
        if self.rating < 1 or self.rating > 5:  # Check for valid range
            raise ValidationError("Rating must be between 1 and 5.")
        if not isinstance(self.hourly_pay, str):
            raise ValidationError("Hourly Pay must be a string.")
        if self.review is None:
            raise ValidationError("Review cannot be null.")
        if not isinstance(self.review, str):
            raise ValidationError("Review must be a string.")
    # Reference to the User model using ForeignKey
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    class Meta:
        # pylint: disable=R0903
        """Meta options for the Reviews model."""
        verbose_name_plural = "Reviews"
# pylint: disable=R0903


class Vacancies(models.Model):
    """Model that stores information about job vacancies.

    Attributes:
        jobTitle (str): The title of the job vacancy.
        jobDescription (str): A description of the job vacancy.
        jobLocation (str): The location of the job vacancy.
        jobPayRate (str): The pay rate for the job vacancy.
        maxHoursAllowed (int): The maximum hours allowed for the job vacancy.
    """

    # vacancyId = models.AutoField(primary_key=True)  # Unique ID for each
    # vacancy
    jobTitle = models.CharField(max_length=500, db_index=True) # Job title
    jobDescription = models.CharField(max_length=1000, db_index=True) # Description of the vacancy
    jobLocation = models.CharField(max_length=500, db_index=True) # Job location
    jobPayRate = models.CharField(max_length=120, db_index=True) # Pay rate
    maxHoursAllowed = models.IntegerField() # Maximum hours allowed for job

    # def __init__(self, jobTitle, jobDescription, jobLocation, jobPayRate, maxHoursAllowed):
    #     super().__init__()  # Call the parent constructor
    #     self.jobTitle = jobTitle
    #     self.jobDescription = jobDescription
    #     self.jobLocation = jobLocation
    #     self.jobPayRate = jobPayRate
    #     self.maxHoursAllowed = maxHoursAllowed

    class Meta:
        """Meta options for the Vacancies model."""
        verbose_name_plural = "Vacancies" # Specify plural name for admin
