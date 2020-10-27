import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Movie, Comment
from .factories import MovieFactory, CommentFactory


"""
I wanted to created mocking with factory_boy but for some reason it was not working properly.
Because of lack of time I need to leave it this way.
"""


class MovieTests(APITestCase):

    def setUp(self):
        self.url = reverse('movie-list')
        self.data = {'title': 'Thor'}
        self.wrong_data = {'title': 'gnoivfd'}

    def test_post_movie(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Movie.objects.get().title, self.data['title'])
        self.assertEqual(Movie.objects.get().year, 2011)
        self.assertEqual(Movie.objects.get().imdb_id, 'tt0800369')
        self.assertEqual(Movie.objects.get().type, 'movie')
        self.assertEqual(Movie.objects.get().poster,
                         'https://m.media-amazon.com/images/M/'
                         'MV5BOGE4NzU1YTAtNzA3Mi00ZTA2LTg2YmYtMDJmMThiMjlkYjg2XkEyXkFqcGdeQXVyNTgzMDMzMTg@.'
                         '_V1_SX300.jpg')

    def test_post_wrong_title(self):
        response = self.client.post(self.url, self.wrong_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_movie(self):
        self.client.post(self.url, self.data, format='json')
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(json.loads(response.content)[0]['title'], 'Thor')


class MoviePutDeleteTest(APITestCase):

    def setUp(self):
        self.client.post(reverse('movie-list'), {'title': 'Thor'}, format='json')
        self.url = reverse('movie', kwargs={'id': 1})
        self.wrong_url = reverse('movie', kwargs={'id': 2})
        self.data = {'year': 3000}
        self.wrong_data = {'year': 'string'}

    def test_put_movie(self):
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Movie.objects.get().year, self.data['year'])
        self.assertNotEqual(Movie.objects.get().year, 2011)

    def test_put_wrong_value(self):
        response = self.client.put(self.url, self.wrong_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_movie(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_wrong_movie_id(self):
        response = self.client.delete(self.wrong_url)
        self.assertEqual(response.status_code, 404)
        self.assertNotEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CommentTests(APITestCase):

    def setUp(self):
        self.client.post('/movies/', {'title': 'Thor'}, format='json')
        self.url = reverse('comment-list')
        self.data = {'movie_id': 1, 'body': 'LoremIpsum'}
        self.wrong_data = {'movie_id': 1, 'body': {4332324: 'fdsdsf'}}

    def test_post_comment(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.get().movie.id, self.data['movie_id'])
        self.assertEqual(Comment.objects.get().body, self.data['body'])

    def test_post_wrong_value(self):
        response = self.client.post(self.url, self.wrong_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)

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
        self.client.post('/movies/', {'title': 'Thor'}, format='json')
        self.client.post('/movies/', {'title': 'Matrix'}, format='json')
        self.client.post('/movies/', {'title': 'Star Wars'}, format='json')
        self.client.post('/movies/', {'title': 'Red'}, format='json')
        self.client.post('/comments/', {'movie_id': 1, 'body': 'LoremIpsum'}, format='json')
        self.client.post('/comments/', {'movie_id': 1, 'body': 'LoremIpsum'}, format='json')
        self.client.post('/comments/', {'movie_id': 2, 'body': 'LoremIpsum'}, format='json')
        self.client.post('/comments/', {'movie_id': 2, 'body': 'LoremIpsum'}, format='json')
        self.client.post('/comments/', {'movie_id': 2, 'body': 'LoremIpsum'}, format='json')
        self.client.post('/comments/', {'movie_id': 2, 'body': 'LoremIpsum'}, format='json')
        self.client.post('/comments/', {'movie_id': 4, 'body': 'LoremIpsum'}, format='json')
        self.client.post('/comments/', {'movie_id': 3, 'body': 'LoremIpsum'}, format='json')

    def test_get_top(self):
        response = self.client.get('/top/?date_start=2020-04-17T00:00:00.000Z&date_end=2021-04-19T00:00:00.000Z', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content)[0]['movie_id'], 2)
        self.assertEqual(json.loads(response.content)[2]['rank'], 3)
        self.assertEqual(json.loads(response.content)[1]['rank'], 2)
        self.assertEqual(json.loads(response.content)[0]['rank'], 1)
        self.assertEqual(json.loads(response.content)[2]['total_comments'], 1)
        self.assertEqual(json.loads(response.content)[1]['total_comments'], 2)
        self.assertEqual(len(response.data), 3)
        self.assertNotEqual(json.loads(response.content)[0]['movie_id'], 22)
        self.assertNotEqual(json.loads(response.content)[2]['rank'], 33)
        self.assertNotEqual(json.loads(response.content)[1]['rank'], 12)
        self.assertNotEqual(json.loads(response.content)[0]['rank'], 31)
        self.assertNotEqual(json.loads(response.content)[2]['total_comments'], 41)
        self.assertNotEqual(json.loads(response.content)[1]['total_comments'], 52)
        self.assertNotEqual(len(response.data), 4)
