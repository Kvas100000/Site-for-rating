from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Movie, Rating
from .forms import RatingForm

User = get_user_model()

class RateItTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='testpassword123')
        self.movie = Movie.objects.create(
            title="Тестовый фильм",
            slug="test-film",
            description="Описание тестового фильма",
            release_year=2024,
            category='MOVIE',
            duration = 120
        )

    def test_model_create_read_delete(self):
        movie_from_db = Movie.objects.get(slug="test-film")
        self.assertEqual(movie_from_db.title, "Тестовый фильм")

        new_movie = Movie.objects.create(
            title="Другой фильм",
            slug="other-film",
            release_year=2023,
            duration=90
        )
        self.assertEqual(Movie.objects.count(), 2)

        new_movie.delete()
        self.assertEqual(Movie.objects.count(), 1)

    def test_get_average_score_method(self):
        Rating.objects.create(user=self.user, content=self.movie, score=8, status='WATCHED')

        user2 = User.objects.create_user(username='tester2', password='123')
        Rating.objects.create(user=user2, content=self.movie, score=10, status='WATCHED')

        average = self.movie.get_average_score()
        self.assertEqual(average, 9.0)

    def test_content_detail_view(self):
        url = reverse('main:content_detail', args=[self.movie.slug])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_pages/detail.html')
        self.assertEqual(response.context['item'].title, "Тестовый фильм")

    def test_rating_form_valid_data(self):
        form_data = {
            'score': 9,
            'status': 'WATCHED',
            'review': 'Крутой фильм!'
        }
        form = RatingForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_rating_form_invalid_data(self):
        form_data = {
            'score': 15,
            'status': 'WATCHED',
            'review': 'Текст'
        }
        form = RatingForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('score', form.errors)