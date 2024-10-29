from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Reviews, Vacancies
from .serializers import ReviewsSerializer, VacanciesSerializer


class ReviewsModelTest(TestCase):
    def setUp(self):
        self.valid_review_data = {
            'department': 'IT',
            'locations': 'Remote',
            'job_title': 'Software Engineer',
            'job_description': 'Develop software.',
            'hourly_pay': '30',
            'benefits': 'Health Insurance',
            'review': 'Great place to work!',
            'rating': 5,
            'recommendation': 1
        }

    def test_create_review(self):
        review = Reviews.objects.create(**self.valid_review_data)
        self.assertEqual(review.department, 'IT')

    def test_review_validation_empty_department(self):
        with self.assertRaises(Exception):  # Adjust exception type as needed
            Reviews.objects.create(
                locations='Remote',
                job_title='Software Engineer',
                job_description='Develop software.',
                hourly_pay='30',
                benefits='Health Insurance',
                review='Great place to work!',
                rating=5,
                recommendation=1
            )

    def test_review_validation_empty_job_title(self):
        with self.assertRaises(Exception):  # Adjust exception type as needed
            Reviews.objects.create(
                department='IT',
                locations='Remote',
                job_description='Develop software.',
                hourly_pay='30',
                benefits='Health Insurance',
                review='Great place to work!',
                rating=5,
                recommendation=1
            )

    def test_review_validation_empty_hourly_pay(self):
        with self.assertRaises(Exception):  # Adjust exception type as needed
            Reviews.objects.create(
                department='IT',
                locations='Remote',
                job_title='Software Engineer',
                job_description='Develop software.',
                benefits='Health Insurance',
                review='Great place to work!',
                rating=5,
                recommendation=1
            )

    def test_review_validation_empty_review(self):
        with self.assertRaises(Exception):  # Adjust exception type as needed
            Reviews.objects.create(
                department='IT',
                locations='Remote',
                job_title='Software Engineer',
                job_description='Develop software.',
                hourly_pay='30',
                benefits='Health Insurance',
                rating=5,
                recommendation=1
            )

    def test_review_validation_empty_rating(self):
        with self.assertRaises(Exception):  # Adjust exception type as needed
            Reviews.objects.create(
                department='IT',
                locations='Remote',
                job_title='Software Engineer',
                job_description='Develop software.',
                hourly_pay='30',
                benefits='Health Insurance',
                review='Great place to work!',
                recommendation=1
            )


class VacanciesModelTest(TestCase):
    def setUp(self):
        self.valid_vacancy_data = {
            'jobTitle': 'Software Engineer',
            'jobDescription': 'Develop software.',
            'jobLocation': 'Remote',
            'jobPayRate': '30',
            'maxHoursAllowed': 40
        }

    def test_create_vacancy(self):
        vacancy = Vacancies.objects.create(**self.valid_vacancy_data)
        self.assertEqual(vacancy.jobTitle, 'Software Engineer')

    def test_vacancy_validation_empty_job_title(self):
        with self.assertRaises(Exception):  # Adjust exception type as needed
            Vacancies.objects.create(
                jobDescription='Develop software.',
                jobLocation='Remote',
                jobPayRate='30',
                maxHoursAllowed=40
            )

    def test_vacancy_validation_empty_job_description(self):
        with self.assertRaises(Exception):  # Adjust exception type as needed
            Vacancies.objects.create(
                jobTitle='Software Engineer',
                jobLocation='Remote',
                jobPayRate='30',
                maxHoursAllowed=40
            )

    def test_vacancy_validation_empty_job_location(self):
        with self.assertRaises(Exception):  # Adjust exception type as needed
            Vacancies.objects.create(
                jobTitle='Software Engineer',
                jobDescription='Develop software.',
                jobPayRate='30',
                maxHoursAllowed=40
            )

    def test_vacancy_validation_empty_job_pay_rate(self):
        with self.assertRaises(Exception):  # Adjust exception type as needed
            Vacancies.objects.create(
                jobTitle='Software Engineer',
                jobDescription='Develop software.',
                jobLocation='Remote',
                maxHoursAllowed=40
            )

    def test_vacancy_validation_max_hours_allowed_zero(self):
        with self.assertRaises(Exception):  # Adjust exception type as needed
            Vacancies.objects.create(
                jobTitle='Software Engineer',
                jobDescription='Develop software.',
                jobLocation='Remote',
                jobPayRate='30',
                maxHoursAllowed=0
            )


class ReviewsSerializerTest(TestCase):
    def setUp(self):
        self.valid_review_data = {
            'department': 'IT',
            'locations': 'Remote',
            'job_title': 'Software Engineer',
            'job_description': 'Develop software.',
            'hourly_pay': '30',
            'benefits': 'Health Insurance',
            'review': 'Great place to work!',
            'rating': 5,
            'recommendation': 1
        }
        self.serializer = ReviewsSerializer(data=self.valid_review_data)

    def test_serializer_valid_data(self):
        self.assertTrue(self.serializer.is_valid())

    def test_serializer_invalid_rating(self):
        self.serializer = ReviewsSerializer(data={**self.valid_review_data, 'rating': 6})
        self.assertFalse(self.serializer.is_valid())
        self.assertIn('rating', self.serializer.errors)

    def test_serializer_empty_review(self):
        self.serializer = ReviewsSerializer(data={**self.valid_review_data, 'review': ''})
        self.assertFalse(self.serializer.is_valid())
        self.assertIn('review', self.serializer.errors)


class VacanciesSerializerTest(TestCase):
    def setUp(self):
        self.valid_vacancy_data = {
            'jobTitle': 'Software Engineer',
            'jobDescription': 'Develop software.',
            'jobLocation': 'Remote',
            'jobPayRate': '30',
            'maxHoursAllowed': 40
        }
        self.serializer = VacanciesSerializer(data=self.valid_vacancy_data)

    def test_serializer_valid_data(self):
        self.assertTrue(self.serializer.is_valid())

    def test_serializer_empty_job_title(self):
        self.serializer = VacanciesSerializer(data={**self.valid_vacancy_data, 'jobTitle': ''})
        self.assertFalse(self.serializer.is_valid())
        self.assertIn('jobTitle', self.serializer.errors)

    def test_serializer_empty_job_description(self):
        self.serializer = VacanciesSerializer(data={**self.valid_vacancy_data, 'jobDescription': ''})
        self.assertFalse(self.serializer.is_valid())
        self.assertIn('jobDescription', self.serializer.errors)

    def test_serializer_max_hours_allowed_zero(self):
        self.serializer = VacanciesSerializer(data={**self.valid_vacancy_data, 'maxHoursAllowed': 0})
        self.assertFalse(self.serializer.is_valid())
        self.assertIn('maxHoursAllowed', self.serializer.errors)


class ReviewsViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_review_data = {
            'department': 'IT',
            'locations': 'Remote',
            'job_title': 'Software Engineer',
            'job_description': 'Develop software.',
            'hourly_pay': '30',
            'benefits': 'Health Insurance',
            'review': 'Great place to work!',
            'rating': 5,
            'recommendation': 1
        }
        self.review = Reviews.objects.create(**self.valid_review_data)

    def test_list_reviews(self):
        response = self.client.get('/api/reviews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_review(self):
        response = self.client.post('/api/reviews/', self.valid_review_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_review_invalid(self):
        invalid_data = self.valid_review_data.copy()
        invalid_data['rating'] = 6
        response = self.client.post('/api/reviews/', invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_review(self):
        updated_data = {'review': 'Updated review'}
        response = self.client.put(f'/api/reviews/{self.review.id}/', updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.review, 'Updated review')

    def test_delete_review(self):
        response = self.client.delete(f'/api/reviews/{self.review.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Reviews.objects.filter(id=self.review.id).exists())


class VacanciesViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_vacancy_data = {
            'jobTitle': 'Software Engineer',
            'jobDescription': 'Develop software.',
            'jobLocation': 'Remote',
            'jobPayRate': '30',
            'maxHoursAllowed': 40
        }
        self.vacancy = Vacancies.objects.create(**self.valid_vacancy_data)

    def test_list_vacancies(self):
        response = self.client.get('/api/vacancies/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

