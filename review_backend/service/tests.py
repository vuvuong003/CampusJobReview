"""
Tests for the 'service' application.

This module contains test cases for the views, models, and serializers
within the 'service' app. It uses Django's testing framework and the
REST framework's testing tools to ensure the application's components
function as expected.
"""

# from django.test import TestCase
from django.test import TestCase
from .models import Reviews
from django.core.exceptions import ValidationError


class ReviewsTests(TestCase):

    def setUp(self):
        """Setup data for each test to ensure isolation."""
        self.review_1 = Reviews.objects.create(
            department="IT",
            locations="Remote",
            job_title="Software Engineer",
            job_description="Develop software.",
            hourly_pay="30",
            benefits="Health Insurance",
            review="Great place to work!",
            rating=5,
            recommendation=1
        )
        self.review_2 = Reviews.objects.create(
            department="HR",
            locations="On-site",
            job_title="HR Manager",
            job_description="Manage HR processes.",
            hourly_pay="40",
            benefits="Life Insurance",
            review="Good work environment.",
            rating=4,
            recommendation=1
        )
        self.review_3 = Reviews.objects.create(
            department="IT",
            locations="Remote",
            job_title="Data Scientist",
            job_description="Analyze data.",
            hourly_pay="35",
            benefits="Health Insurance",
            review="Challenging tasks.",
            rating=3,
            recommendation=1
        )

    ### Basic Field Validation: 8 tests

    def test_department_not_empty(self):
        """Test that department cannot be empty."""
        with self.assertRaises(ValidationError):
            review = Reviews(department="", job_title="Engineer", hourly_pay="30", review="Nice", rating=4, recommendation=1)
            review.full_clean()

    def test_locations_not_empty(self):
        """Test that locations cannot be empty."""
        with self.assertRaises(ValidationError):
            review = Reviews(department="IT", locations="", job_title="Engineer", hourly_pay="30", review="Nice", rating=4, recommendation=1)
            review.full_clean()

    def test_job_title_not_empty(self):
        """Test that job_title cannot be empty."""
        with self.assertRaises(ValidationError):
            review = Reviews(department="IT", job_title="", locations="Remote", hourly_pay="30", review="Nice", rating=4, recommendation=1)
            review.full_clean()

    def test_hourly_pay_not_empty(self):
        """Test that hourly_pay cannot be empty."""
        with self.assertRaises(ValidationError):
            review = Reviews(department="IT", job_title="Engineer", locations="Remote", hourly_pay="", review="Nice", rating=4, recommendation=1)
            review.full_clean()

    def test_benefits_not_empty(self):
        """Test that benefits cannot be empty."""
        with self.assertRaises(ValidationError):
            review = Reviews(department="IT", job_title="Engineer", locations="Remote", hourly_pay="30", benefits="", review="Nice", rating=4, recommendation=1)
            review.full_clean()

    def test_review_not_empty(self):
        """Test that review cannot be empty."""
        with self.assertRaises(ValidationError):
            review = Reviews(department="IT", job_title="Engineer", locations="Remote", hourly_pay="30", benefits="Health Insurance", review="", rating=4, recommendation=1)
            review.full_clean()

    def test_rating_not_null(self):
        """Test that rating cannot be null."""
        with self.assertRaises(ValidationError):
            review = Reviews(department="IT", job_title="Engineer", locations="Remote", hourly_pay="30", benefits="Health Insurance", review="Nice", rating=None, recommendation=1)
            review.full_clean()

    def test_invalid_rating_above_max(self):
        """Test that rating cannot exceed 5."""
        with self.assertRaises(ValidationError):
            review = Reviews(department="IT", job_title="Engineer", locations="Remote", hourly_pay="30", benefits="Health Insurance", review="Nice", rating=6, recommendation=1)
            review.full_clean()

    def test_invalid_rating_below_min(self):
        """Test that rating cannot be less than 1."""
        with self.assertRaises(ValidationError):
            review = Reviews(department="IT", job_title="Engineer", locations="Remote", hourly_pay="30", benefits="Health Insurance", review="Nice", rating=0, recommendation=1)
            review.full_clean()

    ### Data Integrity and Creation Tests: 3 tests

    def test_create_review(self):
        """Test that a review can be created successfully."""
        review = Reviews.objects.create(
            department="Marketing",
            locations="On-site",
            job_title="Brand Manager",
            job_description="Manage brand.",
            hourly_pay="50",
            benefits="Retirement Plan",
            review="Innovative team.",
            rating=5,
            recommendation=1
        )
        self.assertEqual(review.department, "Marketing")

    def test_delete_review(self):
        """Test that a review can be deleted successfully."""
        initial_count = Reviews.objects.count()
        self.review_1.delete()
        self.assertEqual(Reviews.objects.count(), initial_count - 1)

    def test_review_fields(self):
        """Test that all fields of a review are set correctly."""
        self.assertEqual(self.review_1.department, "IT")
        self.assertEqual(self.review_1.locations, "Remote")
        self.assertEqual(self.review_1.job_title, "Software Engineer")
        self.assertEqual(self.review_1.job_description, "Develop software.")
        self.assertEqual(self.review_1.hourly_pay, "30")
        self.assertEqual(self.review_1.benefits, "Health Insurance")
        self.assertEqual(self.review_1.review, "Great place to work!")
        self.assertEqual(self.review_1.rating, 5)
        self.assertEqual(self.review_1.recommendation, 1)

    ### Filtering/Query Tests: 7 tests

    def test_filter_by_location(self):
        """Test filtering reviews by location."""
        remote_reviews = Reviews.objects.filter(locations="Remote")
        self.assertEqual(remote_reviews.count(), 2)

    def test_filter_by_department(self):
        """Test filtering reviews by department."""
        it_reviews = Reviews.objects.filter(department="IT")
        self.assertEqual(it_reviews.count(), 2)

    def test_filter_by_hourly_pay(self):
        """Test filtering reviews by hourly pay."""
        reviews_30 = Reviews.objects.filter(hourly_pay="30")
        self.assertEqual(reviews_30.count(), 1)
        self.assertEqual(reviews_30.first(), self.review_1)

    def test_filter_by_rating(self):
        """Test filtering reviews by rating."""
        high_rating_reviews = Reviews.objects.filter(rating__gte=4)
        self.assertEqual(high_rating_reviews.count(), 2)
        self.assertIn(self.review_1, high_rating_reviews)
        self.assertIn(self.review_2, high_rating_reviews)

    def test_filter_by_benefits(self):
        """Test filtering reviews by benefits."""
        insurance_reviews = Reviews.objects.filter(benefits="Health Insurance")
        self.assertEqual(insurance_reviews.count(), 2)  # Two reviews with Health Insurance

    def test_filter_by_job_title(self):
        """Test filtering reviews by job title."""
        engineer_reviews = Reviews.objects.filter(job_title="Engineer")
        self.assertEqual(engineer_reviews.count(), 1)  # Assuming both review_1 and review_3 have job titles with "Engineer"

    def test_filter_by_recommendation(self):
        """Test filtering reviews by recommendation."""
        recommended_reviews = Reviews.objects.filter(recommendation=1)
        self.assertEqual(recommended_reviews.count(), 3)

    ### Edge Cases: 5 tests

    def test_empty_string_department(self):
        """Test that department cannot be an empty string."""
        with self.assertRaises(ValidationError):
            review = Reviews(
                department="",
                locations="On-site",
                job_title="Engineer",
                job_description="Analyze data",
                hourly_pay="30",
                benefits="Health Insurance",
                review="Good place to work.",
                rating=3,
                recommendation=1
            )
            review.full_clean()

    def test_max_length_exceeded(self):
        """Test that a field cannot exceed its maximum length."""
        with self.assertRaises(ValidationError):
            review = Reviews(
                department="A" * 101,  # Exceeding max length of 100
                locations="On-site",
                job_title="Analyst",
                job_description="Analyze finances.",
                hourly_pay="40",
                benefits="Pension",
                review="Good place to work.",
                rating=3,
                recommendation=1
            )
            review.full_clean()

    def test_review_with_special_characters(self):
        """Test that special characters are handled correctly in reviews."""
        review = Reviews(
            department="IT",
            locations="Remote",
            job_title="Engineer",
            job_description="Develop software.",
            hourly_pay="30",
            benefits="Health Insurance",
            review="Nice place to work! 😊",  # Special character
            rating=4,
            recommendation=1
        )
        review.full_clean()  # Should not raise an error

    def test_review_creation_without_recommendation(self):
        """Test that a review can be created without a recommendation value."""
        review = Reviews.objects.create(
            department="IT",
            locations="Remote",
            job_title="Engineer",
            job_description="Develop software.",
            hourly_pay="30",
            benefits="Health Insurance",
            review="Nice place to work!",
            rating=4
            # No recommendation provided
        )
        self.assertIsNotNone(review.id)  # Should be created successfully

    def test_review_creation_with_zero_rating(self):
        """Test that a review cannot be created with a rating of zero."""
        with self.assertRaises(ValidationError):
            review = Reviews(
                department="IT",
                locations="Remote",
                job_title="Engineer",
                job_description="Develop software.",
                hourly_pay="30",
                benefits="Health Insurance",
                review="Nice place to work!",
                rating=0,  # Invalid rating
                recommendation=1
            )
            review.full_clean()

# from django.test import TestCase
# from .models import Reviews
# from django.core.exceptions import ValidationError

# class ReviewsTests(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.valid_review_data = {
#             'department': 'IT',
#             'locations': 'Remote',
#             'job_title': 'Software Engineer',
#             'job_description': 'Develop software.',
#             'hourly_pay': '30',
#             'benefits': 'Health Insurance',
#             'review': 'Great place to work!',
#             'rating': 5,
#             'recommendation': 1
#         }

#     # -----------------------------
#     # Basic Field Validation Tests (8 tests)
#     # -----------------------------

#     def test_department_required(self):
#         data = self.valid_review_data.copy()
#         data['department'] = None
#         review = Reviews(**data)
#         with self.assertRaises(ValidationError):
#             review.full_clean()

#     def test_job_title_required(self):
#         data = self.valid_review_data.copy()
#         data['job_title'] = None
#         review = Reviews(**data)
#         with self.assertRaises(ValidationError):
#             review.full_clean()

#     def test_hourly_pay_required(self):
#         data = self.valid_review_data.copy()
#         data['hourly_pay'] = None
#         review = Reviews(**data)
#         with self.assertRaises(ValidationError):
#             review.full_clean()

#     def test_review_required(self):
#         data = self.valid_review_data.copy()
#         data['review'] = None
#         review = Reviews(**data)
#         with self.assertRaises(ValidationError):
#             review.full_clean()

#     def test_rating_required(self):
#         data = self.valid_review_data.copy()
#         data['rating'] = None
#         review = Reviews(**data)
#         with self.assertRaises(ValidationError):
#             review.full_clean()

#     def test_rating_min_value(self):
#         data = self.valid_review_data.copy()
#         data['rating'] = 0  # Invalid: less than 1
#         review = Reviews(**data)
#         with self.assertRaises(ValidationError):
#             review.full_clean()

#     def test_rating_max_value(self):
#         data = self.valid_review_data.copy()
#         data['rating'] = 6  # Invalid: greater than 5
#         review = Reviews(**data)
#         with self.assertRaises(ValidationError):
#             review.full_clean()

#     def test_max_length_constraints(self):
#         max_lengths = {
#             'department': 100,
#             'locations': 120,
#             'job_title': 64,
#             'job_description': 120,
#             'hourly_pay': 10,
#             'benefits': 120,
#             'review': 120,
#         }
#         for field, max_length in max_lengths.items():
#             data = self.valid_review_data.copy()
#             data[field] = 'x' * (max_length + 1)  # Exceed max length
#             review = Reviews(**data)
#             with self.assertRaises(ValidationError):
#                 review.full_clean()

#     # -----------------------------
#     # Data Integrity and Creation Tests (3 tests)
#     # -----------------------------

#     def test_create_valid_review(self):
#         review = Reviews.objects.create(**self.valid_review_data)
#         self.assertEqual(review.department, 'IT')
#         self.assertEqual(review.job_title, 'Software Engineer')
#         self.assertEqual(review.rating, 5)

#     def test_update_review_data(self):
#         review = Reviews.objects.create(**self.valid_review_data)
#         review.job_title = 'Senior Engineer'
#         review.rating = 4
#         review.save()
#         self.assertEqual(review.job_title, 'Senior Engineer')
#         self.assertEqual(review.rating, 4)

#     def test_delete_review(self):
#         review = Reviews.objects.create(**self.valid_review_data)
#         review_id = review.id
#         review.delete()
#         self.assertFalse(Reviews.objects.filter(id=review_id).exists())

#     # -----------------------------
#     # Filtering and Query Tests (7 tests)
#     # -----------------------------

#     def setUp(self):
#         self.review_1 = Reviews.objects.create(**self.valid_review_data)
#         self.review_2 = Reviews.objects.create(
#             department="HR", locations="On-site", job_title="HR Manager",
#             job_description="Manage HR", hourly_pay="40", benefits="Dental Insurance",
#             review="Good environment", rating=4, recommendation=1
#         )
#         self.review_3 = Reviews.objects.create(
#             department="IT", locations="Remote", job_title="Data Scientist",
#             job_description="Analyze data", hourly_pay="35", benefits="Life Insurance",
#             review="Challenging tasks", rating=3, recommendation=0
#         )

#     def test_filter_by_department(self):
#         it_reviews = Reviews.objects.filter(department='IT')
#         self.assertEqual(it_reviews.count(), 2)

#     def test_filter_by_job_title(self):
#         engineer_reviews = Reviews.objects.filter(job_title='Software Engineer')
#         self.assertEqual(engineer_reviews.count(), 1)
#         self.assertEqual(engineer_reviews.first(), self.review_1)

#     def test_filter_by_hourly_pay(self):
#         reviews_40_pay = Reviews.objects.filter(hourly_pay='40')
#         self.assertEqual(reviews_40_pay.count(), 1)
#         self.assertEqual(reviews_40_pay.first(), self.review_2)

#     def test_filter_by_rating(self):
#         high_rating_reviews = Reviews.objects.filter(rating__gte=4)
#         self.assertEqual(high_rating_reviews.count(), 2)

#     def test_filter_by_location(self):
#         remote_reviews = Reviews.objects.filter(locations="Remote")
#         self.assertEqual(remote_reviews.count(), 2)

#     def test_filter_by_benefits(self):
#         insurance_reviews = Reviews.objects.filter(benefits="Health Insurance")
#         self.assertEqual(insurance_reviews.count(), 1)

#     def test_filter_combined_conditions(self):
#         combined_reviews = Reviews.objects.filter(department="IT", rating__gte=3)
#         self.assertEqual(combined_reviews.count(), 2)

#     # -----------------------------
#     # Edge Case Tests (5 tests)
#     # -----------------------------

#     def test_optional_fields_blank(self):
#         data = self.valid_review_data.copy()
#         data['locations'] = None
#         review = Reviews(**data)
#         try:
#             review.full_clean()
#         except ValidationError:
#             self.fail("Review raised ValidationError unexpectedly!")

#     def test_special_characters_in_review(self):
#         data = self.valid_review_data.copy()
#         data['review'] = "Great place to work! 😊🚀"
#         review = Reviews(**data)
#         try:
#             review.full_clean()
#         except ValidationError:
#             self.fail("Review raised ValidationError unexpectedly with special characters!")

#     def test_boundary_rating_values(self):
#         for rating in [1, 5]:
#             data = self.valid_review_data.copy()
#             data['rating'] = rating
#             review = Reviews(**data)
#             try:
#                 review.full_clean()
#             except ValidationError:
#                 self.fail("Review raised ValidationError unexpectedly for boundary rating values.")

#     def test_large_numeric_hourly_pay(self):
#         data = self.valid_review_data.copy()
#         data['hourly_pay'] = '99999'  # Edge case for high hourly pay
#         review = Reviews(**data)
#         try:
#             review.full_clean()
#         except ValidationError:
#             self.fail("Review raised ValidationError unexpectedly with large numeric hourly pay!")

#     def test_null_recommendation_field(self):
#         data = self.valid_review_data.copy()
#         data['recommendation'] = None  # Optional field set to None
#         review = Reviews(**data)
#         try:
#             review.full_clean()
#         except ValidationError:
#             self.fail("Review raised ValidationError unexpectedly for null recommendation field!")

#     @classmethod
#     def tearDownClass(cls):
#         Reviews.objects.all().delete()
#         super().tearDownClass()
