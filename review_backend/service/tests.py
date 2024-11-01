# """
# This module contains test cases for the Reviews model and its serializer in a Django application.

# The `ReviewsModelTests` class extends `TestCase` to provide a framework for testing
# various aspects of the Reviews model. It includes:

# - **setUp**: Initializes common valid data for testing.
# - **test_department_not_blank**: Ensures the 'department' field cannot be blank.
# - **test_job_title_not_blank**: Ensures the 'job_title' field cannot be blank.
# - **test_hourly_pay_not_blank**: Ensures the 'hourly_pay' field cannot be blank.
# - **test_rating_out_of_range_high**: Ensures 'rating' cannot exceed 5.
# - **test_rating_out_of_range_low**: Ensures 'rating' cannot fall below 1.
# - **test_optional_locations_field**: Validates that the 'locations' field can be empty.
# - **test_optional_job_description_field**: Validates that the 'job_description' field can be empty.
# - **test_invalid_department_length**: Ensures 'department' does not exceed 100 characters.
# - **test_invalid_job_title_length**: Ensures 'job_title' does not exceed 64 characters.
# - **test_valid_full_data**: Confirms that valid data creates a review successfully.
# - **test_filter_reviews_by_department**: Tests filtering reviews by 'department'.
# - **test_filter_reviews_by_rating**: Tests filtering reviews by 'rating'.
# - **test_filter_reviews_by_job_title**: Tests filtering reviews by 'job_title'.
# - **test_review_benefits_field_optional**: Confirms 'benefits' can be empty.
# - **test_invalid_rating_type**: Ensures 'rating' is an integer.
# - **test_optional_recommendation_field**: Validates that 'recommendation' can be null.
# - **test_invalid_rating_value**: Ensures 'rating' is within the range of 1 to 5.
# - **test_empty_string_in_benefits**: Confirms 'benefits' can be an empty string.
# - **test_job_description_character_limit**: Ensures 'job_description' does not exceed 120
# characters.
# - **test_invalid_hourly_pay_length**: Ensures 'hourly_pay' does not exceed 10 characters.
# - **tearDownClass**: Cleans up the database by deleting all reviews after tests.

# This suite helps maintain data integrity and validate the functionality of the Reviews model.
# """
# from django.test import TestCase  # Import Django's TestCase for testing
# from rest_framework.exceptions import ValidationError # Import ValidationError for
# # handling validation issues
# from .models import Reviews # Import Reviews model for creating instances in tests
# from .serializers import ReviewsSerializer # Import serializer for validation and data handling


# # Define test cases for the Reviews model using TestCase from Django
# # pylint: disable=R0904
# class ReviewsModelTests(TestCase):
#     """
#     Test cases for the Reviews model.

#     This class tests various validations and constraints for the Reviews model,
#     ensuring data integrity and correct behavior of the associated serializer.
#     """
#     # pylint: disable=C0103
#     def setUp(self):
#         """Set up common valid data for testing various fields and constraints in each test case."""
#         # Set valid initial data for use in multiple tests
#         self.valid_data = {
#             "department": "IT",
#             "locations": "Remote",
#             "job_title": "Engineer",
#             "job_description": "Handles IT infrastructure",
#             "hourly_pay": "30",
#             "benefits": "Health insurance",
#             "review": "Good work environment",
#             "rating": 4,
#             "recommendation": 1
#         }

#     def test_department_not_blank(self):
#         """Test that 'department' field cannot be blank in the Reviews model."""
#         # Set 'department' to an empty string to test blank validation
#         data = {**self.valid_data, "department": ""}
#         with self.assertRaises(ValidationError): # Expect a validation error
#             ReviewsSerializer(data=data).is_valid(raise_exception=True)

#     def test_job_title_not_blank(self):
#         """Test that 'job_title' field cannot be blank in the Reviews model."""
#         # Set 'job_title' to an empty string to test blank validation
#         data = {**self.valid_data, "job_title": ""}
#         with self.assertRaises(ValidationError): # Expect a validation error
#             ReviewsSerializer(data=data).is_valid(raise_exception=True)

#     def test_hourly_pay_not_blank(self):
#         """Test that 'hourly_pay' field cannot be blank in the Reviews model."""
#         # Set 'hourly_pay' to an empty string to test blank validation
#         data = {**self.valid_data, "hourly_pay": ""}
#         with self.assertRaises(ValidationError): # Expect a validation error
#             ReviewsSerializer(data=data).is_valid(raise_exception=True)

#     def test_rating_out_of_range_high(self):
#         """Test that 'rating' field cannot be set above 5."""
#         # Set 'rating' to 6 to test maximum validation
#         data = {**self.valid_data, "rating": 6}
#         with self.assertRaises(ValidationError): # Expect a validation error
#             ReviewsSerializer(data=data).is_valid(raise_exception=True)

#     def test_rating_out_of_range_low(self):
#         """Test that 'rating' field cannot be set below 1."""
#         # Set 'rating' to 0 to test minimum validation
#         data = {**self.valid_data, "rating": 0}
#         with self.assertRaises(ValidationError): # Expect a validation error
#             ReviewsSerializer(data=data).is_valid(raise_exception=True)

#     # def test_optional_review_field(self):
#     #     """Test that 'review' can be empty and still valid."""
#     #     data = {**self.valid_data, "review": ""}
#     #     serializer = ReviewsSerializer(data=data)
#     #     self.assertTrue(serializer.is_valid())
#     #     print(serializer.errors)

#     def test_optional_locations_field(self):
#         """Test that 'locations' can be empty and still valid."""
#         # Set 'locations' to an empty string
#         data = {**self.valid_data, "locations": ""}
#         serializer = ReviewsSerializer(data=data) # Validate data
#         self.assertTrue(serializer.is_valid()) # Confirm data is valid

#     def test_optional_job_description_field(self):
#         """Test that 'job_description' can be empty and still valid."""
#         # Set 'job_description' to an empty string
#         data = {**self.valid_data, "job_description": ""}
#         serializer = ReviewsSerializer(data=data) # Validate data
#         self.assertTrue(serializer.is_valid()) # Confirm data is valid

#     def test_invalid_department_length(self):
#         """Test that 'department' cannot exceed max length of 100 characters."""
#         # Set 'department' to a string of 101 characters
#         data = {**self.valid_data, "department": "A" * 101}
#         with self.assertRaises(ValidationError): # Validate data
#             ReviewsSerializer(data=data).is_valid(raise_exception=True) # Confirm data is valid

#     def test_invalid_job_title_length(self):
#         """Test that 'job_title' cannot exceed max length of 64 characters."""
#         # Set 'job_title' to a string of 65 characters
#         data = {**self.valid_data, "job_title": "A" * 65}
#         with self.assertRaises(ValidationError): # Expect a validation error
#             ReviewsSerializer(data=data).is_valid(raise_exception=True)

#     # def test_invalid_hourly_pay_type(self):
#     #     """Test that 'hourly_pay' must be a string, not a number."""
#     #     with self.assertRaises(ValidationError):
#     #         review = Reviews(
#     #             department="IT",
#     #             job_title="Engineer",
#     #             hourly_pay=30,  # Incorrect type: number instead of string
#     #             review="Nice",
#     #             rating=4,
#     #             recommendation=1
#     #         )
#     #     review.full_clean()

#     def test_valid_full_data(self):
#         """Test that valid data creates a review successfully."""
#         # Validate data with all fields filled correctly
#         serializer = ReviewsSerializer(data=self.valid_data)
#         self.assertTrue(serializer.is_valid())

#     def test_filter_reviews_by_department(self):
#         """Test filtering reviews by 'department'."""
#         # Create two review instances with different departments
#         # pylint: disable=E1101
#         review1 = Reviews.objects.create(**self.valid_data)
#         # pylint: disable=E1101
#         review2 = Reviews.objects.create(**{**self.valid_data, "department": "HR"})
#         # Filter reviews by department and check presence of each review
#         # pylint: disable=E1101
#         it_reviews = Reviews.objects.filter(department="IT")
#         # pylint: disable=E1101
#         hr_reviews = Reviews.objects.filter(department="HR")
#         self.assertIn(review1, it_reviews)
#         self.assertIn(review2, hr_reviews)

#     def test_filter_reviews_by_rating(self):
#         """Test filtering reviews by 'rating'."""
#         # Create two review instances with different ratings
#         # pylint: disable=E1101
#         review1 = Reviews.objects.create(**self.valid_data)
#         # pylint: disable=E1101
#         review2 = Reviews.objects.create(**{**self.valid_data, "rating": 5})
#         # Filter reviews by rating and check presence of each review
#         # pylint: disable=E1101
#         high_rating_reviews = Reviews.objects.filter(rating=5) # filter reviews
#         # pylint: disable=E1101
#         low_rating_reviews = Reviews.objects.filter(rating=4) # filter reviews
#         self.assertIn(review2, high_rating_reviews) # Validate data
#         self.assertIn(review1, low_rating_reviews) # Validate data

#     def test_filter_reviews_by_job_title(self):
#         """Test filtering reviews by 'job_title'."""
#         # pylint: disable=E1101
#         review1 = Reviews.objects.create(**self.valid_data)
#         # pylint: disable=E1101
#         review2 = Reviews.objects.create(**{**self.valid_data, "job_title": "Manager"})
#         # pylint: disable=E1101
#         engineer_reviews = Reviews.objects.filter(job_title="Engineer") # filter reviews
#         # pylint: disable=E1101
#         manager_reviews = Reviews.objects.filter(job_title="Manager") # filter reviews
#         self.assertIn(review1, engineer_reviews) # Validate data
#         self.assertIn(review2, manager_reviews) # Validate data

#     def test_review_benefits_field_optional(self):
#         """Test 'benefits' can be blank and still valid."""
#         # Set 'benefits' to an empty string
#         data = {**self.valid_data, "benefits": ""}
#         serializer = ReviewsSerializer(data=data) # Validate data
#         self.assertTrue(serializer.is_valid()) # Confirm data is valid

#     def test_invalid_rating_type(self):
#         """Test 'rating' must be an integer."""
#         # Set 'rating' to 10, which is above the valid range
#         data = {**self.valid_data, "rating": "high"}
#         with self.assertRaises(ValidationError): # Expect a validation error
#             ReviewsSerializer(data=data).is_valid(raise_exception=True)

#     def test_optional_recommendation_field(self):
#         """Test that 'recommendation' can be null and still valid."""
#         data = {**self.valid_data, "recommendation": None}
#         serializer = ReviewsSerializer(data=data) # Validate data
#         self.assertTrue(serializer.is_valid())

#     def test_invalid_rating_value(self):
#         """Test that 'rating' must be within 1 and 5 inclusive."""
#         data = {**self.valid_data, "rating": 10}
#         with self.assertRaises(ValidationError): # Expect a validation error
#             ReviewsSerializer(data=data).is_valid(raise_exception=True)

#     def test_empty_string_in_benefits(self):
#         """Test that 'benefits' can be an empty string."""
#         data = {**self.valid_data, "benefits": ""}
#         serializer = ReviewsSerializer(data=data) # Validate data
#         self.assertTrue(serializer.is_valid())

#     def test_job_description_character_limit(self):
#         """Test that 'job_description' max length is 120 characters."""
#         data = {**self.valid_data, "job_description": "A" * 121}
#         with self.assertRaises(ValidationError):# Expect a validation error
#             ReviewsSerializer(data=data).is_valid(raise_exception=True)

#     # def test_non_string_review_field(self):
#     #     """Test 'review' field should be string."""
#     #     data = {**self.valid_data, "review": 12345}
#     #     with self.assertRaises(ValidationError):
#     #         ReviewsSerializer(data=data).is_valid(raise_exception=True)

#     # def test_valid_hourly_pay_format(self):
#     #     """Test that 'hourly_pay' accepts a string format of a number."""
#     #     data = {**self.valid_data, "hourly_pay": "20"}
#     #     serializer = ReviewsSerializer(data=data)
#     #     self.assertTrue(serializer.is_valid())

#     def test_invalid_hourly_pay_length(self):
#         """Test 'hourly_pay' max length of 10 characters."""
#         # Set 'hourly_pay' to a string of 11 characters
#         data = {**self.valid_data, "hourly_pay": "12345678901"}
#         with self.assertRaises(ValidationError):# Expect a validation error
#             ReviewsSerializer(data=data).is_valid(raise_exception=True)

#     # pylint: disable=C0202,C0103
#     @classmethod
#     def tearDownClass(self):
#         """Clean up the database by deleting all review instances after tests have run."""
#         # pylint: disable=E1101
#         Reviews.objects.all().delete()
#         super().tearDownClass()
