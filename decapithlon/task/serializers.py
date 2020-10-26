from rest_framework import serializers
from task.models import Movie, Comment


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'year', 'type', 'imdb_id', 'poster')
        extra_kwargs = {
            'title': {'required': False},
            'year': {'required': False},
            'type': {'required': False},
            'imdb_id': {'required': False},
            'poster': {'required': False},
        }
        validators = []


class CommentSerializer(serializers.ModelSerializer):
    movie = serializers.SlugRelatedField(slug_field='title', queryset=Movie.objects.all(), required=False)
    movie_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comment
        fields = ('movie', 'body', 'movie_id', 'date')
        extra_kwargs = {
            'movie': {'required': False},
            'date': {'required': False},
        }
        validators = []


class TopSerializer(serializers.Serializer):
    movie_id = serializers.IntegerField()
    total_comments = serializers.IntegerField()
    rank = serializers.IntegerField()
