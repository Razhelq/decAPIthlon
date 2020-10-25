from rest_framework import serializers
from task.models import Movie, Comment


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'year', 'type', 'imdb_id', 'poster')


class CommentSerializer(serializers.ModelSerializer):
    movie = serializers.SlugRelatedField(slug_field='title', queryset=Movie.objects.all(), required=False)
    movie_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comment
        fields = ('movie', 'body', 'movie_id', 'date')


class TopSerializer(serializers.Serializer):
    movie_id = serializers.IntegerField()
    total_comments = serializers.IntegerField()
    rank = serializers.IntegerField()
