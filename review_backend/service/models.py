"""
Module for defining database models for the 'service' application.

This module contains the definitions of the database models used in the
service application, including the Reviews and Vacancies models.
These models represent the data structures for storing review and job
vacancy information in the database.
"""
from djongo import models  # pylint: disable=E0401
# from django.contrib.auth.models import AbstractUser

#pylint: disable=R0903
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
    id = models.AutoField(primary_key=True)  # Use AutoField for unique IDs
    department = models.CharField(max_length=64, db_index=True)
    locations = models.CharField(max_length=120, db_index=True)
    job_title = models.CharField(max_length=64, db_index=True)
    job_description = models.CharField(max_length=120, db_index=True)
    hourly_pay = models.CharField(max_length=10)
    benefits = models.CharField(max_length=120, db_index=True)
    review = models.CharField(max_length=120, db_index=True)
    rating = models.IntegerField()
    recommendation = models.IntegerField()

    # Reference to the User model using ForeignKey
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    class Meta:
        #pylint: disable=R0903
        """Meta options for the Reviews model."""
        verbose_name_plural = "Reviews"
#pylint: disable=R0903
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
    jobTitle = models.CharField(max_length=500, db_index=True)
    jobDescription = models.CharField(max_length=1000, db_index=True)
    jobLocation = models.CharField(max_length=500, db_index=True)
    jobPayRate = models.CharField(max_length=120, db_index=True)
    maxHoursAllowed = models.IntegerField()

    # def __init__(self, jobTitle, jobDescription, jobLocation, jobPayRate, maxHoursAllowed):
    #     super().__init__()  # Call the parent constructor
    #     self.jobTitle = jobTitle
    #     self.jobDescription = jobDescription
    #     self.jobLocation = jobLocation
    #     self.jobPayRate = jobPayRate
    #     self.maxHoursAllowed = maxHoursAllowed

    class Meta:
        """Meta options for the Vacancies model."""
        verbose_name_plural = "Vacancies"
