from djongo import models
from django.contrib.auth.models import AbstractUser


# User Model
# class User(AbstractUser):
#     # Inherits from AbstractUser for Django's built-in user model features
#     image_file = models.CharField(max_length=20, default="default.jpg")

#     def __str__(self):
#         return self.username

# Reviews Model
class Reviews(models.Model):
    """Model which stores the information of the reviews submitted"""

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
        verbose_name_plural = "Reviews"

# Vacancies Model


class Vacancies(models.Model):
    """Model which stores the information of the job vacancies"""

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
        verbose_name_plural = "Vacancies"
