import os
import logging
import requests
from requests.exceptions import ConnectionError
import environ

from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings

from task.models import Movie, Comment
from task.serializers import MovieSerializer, CommentSerializer, TopSerializer


class MovieListView(ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['id', 'title', 'year', 'type', 'imdb_id', 'poster']
    ordering_fields = '__all__'

    def post(self, request):
        data = self.get_movie_details(request.data)
        # if omdbapi is not responding
        if not data:
            content = {'omdbapi not responding': 'nothing to see here'}
            response = Response(content, status=status.HTTP_404_NOT_FOUND)
            return response
        if data == 'Movie not found!':
            content = {'movie not found': 'need correct title'}
            response = Response(content, status=status.HTTP_400_BAD_REQUEST)
            return response
        serializer = MovieSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response

    @staticmethod
    def get_movie_details(data):
        try:
            movie_json = requests.get(f"https://omdbapi.com/?t={data['title']}&apikey={os.environ.get('API_KEY')}").json()
        except ConnectionError:
            return False
        if movie_json['Response'] == 'False':
            return 'Movie not found!'
        else:
            data['title'] = movie_json['Title']
            data['year'] = movie_json['Year'][:4]
            data['imdb_id'] = movie_json['imdbID']
            data['type'] = movie_json['Type']
            data['poster'] = movie_json['Poster']
        return data


class MovieView(APIView):

    def get_object(self, id):
        try:
            return Movie.objects.get(id=id)
        except Movie.DoesNotExist:
            raise Http404

    def put(self, request, id):
        movie = self.get_object(id)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        movie = self.get_object(id)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['movie__id']

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
            return response
        response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response


class TopListView(APIView):

    def get(self, request):
        date_start = request.GET.get('date_start')
        date_end = request.GET.get('date_end')
        if date_start and date_end:
            data = self.count_top(date_start, date_end)
            serializer = TopSerializer(data=data, many=True)
            if serializer.is_valid():
                response = Response(serializer.data)
                return response
        response = Response(
            "Time range is required (date_start, date_end):    e.g. "
            "/top/?date_start=2020-04-17T00:00:00.000Z&date_end=2021-04-19T00:00:00.000Z",
            status=status.HTTP_400_BAD_REQUEST
        )
        return response

    @staticmethod
    def count_top(date_start, date_end):
        top = []
        movies = Movie.objects.filter(comment__date__gte=date_start).filter(comment__date__lte=date_end)
        for movie in movies.distinct():
            comment = Comment.objects.filter(movie=movie).filter(date__gte=date_start).filter(date__lte=date_end)
            top.append({
                'movie_id': movie.id,
                'total_comments': len(comment),
                'rank': 0
            })
        top = sorted(top, key=lambda x: x['total_comments'], reverse=True)
        position = 1
        for x in range(len(top)):
            if x == 0:
                if top[x]['total_comments'] != 0:
                    top[0]['rank'] = position
            else:
                if top[x]['total_comments'] == top[x-1]['total_comments']:
                    top[x]['rank'] = position
                else:
                    position += 1
                    if position == 4:
                        break
                    top[x]['rank'] = position
        new_top = []
        for movie in top:
            if movie['rank'] != 0 and movie['total_comments'] != 0:
                new_top.append(movie)
        return new_top
