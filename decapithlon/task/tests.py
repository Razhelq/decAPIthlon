import json

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Movie, Comment
from rest_framework.test import APIRequestFactory

from .serializers import MovieSerializer


class MovieTests(APITestCase):

    def setUp(self):
        self.url = reverse('movie-list')
        self.data = {'title': 'Thor'}

    def test_post_movie(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.get().title, self.data['title'])
        self.assertEqual(Movie.objects.get().year, 2011)
        self.assertEqual(Movie.objects.get().imdb_id, 'tt0800369')
        self.assertEqual(Movie.objects.get().type, 'movie')
        self.assertEqual(Movie.objects.get().poster,
                         'https://m.media-amazon.com/images/M/'
                         'MV5BOGE4NzU1YTAtNzA3Mi00ZTA2LTg2YmYtMDJmMThiMjlkYjg2XkEyXkFqcGdeQXVyNTgzMDMzMTg@.'
                         '_V1_SX300.jpg')

    def test_get_movie(self):
        self.client.post(self.url, self.data, format='json')
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(json.loads(response.content)[0]['title'], 'Thor')

class CommentTests(APITestCase):

    def setUp(self):
        self.client.post('/movie/', {'title': 'Thor'}, format='json')
        self.url = reverse('comment-list')
        self.data = {'movie_id': 1, 'body': 'LoremIpsum'}

    def test_post_comment(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.get().movie.id, self.data['movie_id'])
        self.assertEqual(Comment.objects.get().body, self.data['body'])

    def test_get_comment(self):
        self.client.post(self.url, self.data, format='json')
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(json.loads(response.content)[0]['movie'], 'Thor')
        self.assertEqual(json.loads(response.content)[0]['body'], self.data['body'])


class TopTests(APITestCase):

    def setUp(self):
        self.client.post('/movie/', {'title': 'Thor'}, format='json')
        self.client.post('/movie/', {'title': 'Matrix'}, format='json')
        self.client.post('/movie/', {'title': 'Star Wars'}, format='json')
        self.client.post('/movie/', {'title': 'Red'}, format='json')
        self.client.post('/comment/', {'movie_id': 1, 'body': 'LoremIpsum'}, format='json')
        self.client.post('/comment/', {'movie_id': 1, 'body': 'LoremIpsum'}, format='json')
        self.client.post('/comment/', {'movie_id': 2, 'body': 'LoremIpsum'}, format='json')
        self.client.post('/comment/', {'movie_id': 2, 'body': 'LoremIpsum'}, format='json')
        self.client.post('/comment/', {'movie_id': 2, 'body': 'LoremIpsum'}, format='json')
        self.client.post('/comment/', {'movie_id': 2, 'body': 'LoremIpsum'}, format='json')
        self.client.post('/comment/', {'movie_id': 4, 'body': 'LoremIpsum'}, format='json')
        self.client.post('/comment/', {'movie_id': 3, 'body': 'LoremIpsum'}, format='json')

    def test_get_comment(self):
        response = self.client.get('/top/?date_start=2020-04-17T00:00:00.000Z&date_end=2021-04-19T00:00:00.000Z', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content)[0]['movie_id'], 2)
        self.assertEqual(json.loads(response.content)[3]['rank'], 3)
        self.assertEqual(json.loads(response.content)[2]['rank'], 3)
        self.assertEqual(json.loads(response.content)[1]['rank'], 1)
        self.assertEqual(json.loads(response.content)[0]['rank'], 2)
        self.assertEqual(json.loads(response.content)[3]['total_comments'], 1)
        self.assertEqual(json.loads(response.content)[1]['total_comments'], 4)
        self.assertEqual(len(response.data), 4)
