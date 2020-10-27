import factory

from .models import Movie, Comment


class MovieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Movie

    title = factory.Sequence(lambda n: 'title%d' % n)
    year = factory.Sequence(lambda n: '%d' % n)
    type = factory.Sequence(lambda n: 'type%d' % n)
    imdb_id = factory.Sequence(lambda n: 'imdb_id%d' % n)
    poster = factory.Sequence(lambda n: 'poster%d' % n)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    first_name = factory.Sequence(lambda n: "comment %d" % n)
    movie = factory.SubFactory(MovieFactory)