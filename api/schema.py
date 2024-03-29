from graphene_django import DjangoObjectType
import graphene
from api.models import Movie,Director

class MovieType(DjangoObjectType):
    class Meta:
        model = Movie

    movie_age = graphene.String()

    def resolve_movie_age(self,info):
        return "Old Movie" if self.year < 2000 else "New Movie"

class DirectorType(DjangoObjectType):
    class Meta:
        model = Director


class Query(graphene.ObjectType):
    all_movies = graphene.List(MovieType)
    movie = graphene.Field(MovieType, id=graphene.Int(), title=graphene.String())
    all_director = graphene.List(DirectorType)

    def resolve_all_movies(self, info, **kwargs):
        return Movie.objects.all()

    def resolve_all_director(self, info, **kwargs):
        return Director.objects.all()

    def resolve_movie(self, info, **kwargs):
        id = kwargs.get('id')
        title = kwargs.get('title')

        if id is not None:
            return Movie.objects.get(pk=id)

        if title is not None:
            return Movie.objects.get(title=title)

        return None

class MovieCreateMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        year = graphene.Int(required=True)

    movie = graphene.Field(MovieType)

    def mutate(self, info, title, year):
        movie = Movie.objects.create(title=title, year=year)

        return MovieCreateMutation(movie=movie)

class MovieUpdateMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        year = graphene.Int()
        id = graphene.ID(required=True)

    movie = graphene.Field(MovieType)

    def mutate(self, info, id, title, year):
        movie = Movie.objects.get(pk=id)

        if title is not None:
            movie.title = title
        if year is not None:
            movie.year = year

        movie.save()

        return MovieUpdateMutation(movie=movie)


class MovieDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    movie = graphene.Field(MovieType)

    def mutate(self, info, id):
        movie = Movie.objects.get(pk=id)
        movie.delete()

        return MovieUpdateMutation(movie=None)



class Mutation:
    create_movie = MovieCreateMutation.Field()
    update_movie = MovieUpdateMutation.Field() 
    delete_movie = MovieDeleteMutation.Field() 