from django.db import models
from django.utils import timezone


class Movie(models.Model):
    title = models.CharField(max_length=128)
    year = models.PositiveIntegerField()
    type = models.CharField(max_length=128)
    imdb_id = models.CharField(max_length=32, unique=True)
    poster = models.TextField()

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    movie = models.ForeignKey(Movie, models.DO_NOTHING)
    body = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.movie} - {self.body}'
