from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from Genre.models import Genre
from .models import Movies
import json
from .serializers import MoviesSerializer
from django.http import Http404
from django.db.models import Q


class LoadJson(APIView):
    """
    Hit this api only once, this api is used to load data from json file into the database.
    """

    def get(self, request, format=None):
        with open('./imdb.json') as json_file:
            movies = json.load(json_file)
            for movie in movies:
                genres = []
                for genre in movie['genre']:
                    genre, created = Genre.objects.get_or_create(name=genre)
                    genres.append(genre)

                movie['popularity'] = movie['99popularity']
                del movie['99popularity']
                del movie['genre']

                movie, created = Movies.objects.get_or_create(**movie)
                if created:
                    for genre in genres:
                        movie.genre.add(genre)
                print(movie)

        return Response(status=status.HTTP_200_OK)


class GetMovies(APIView):
    """
    This will return list of movies depending on page parameter
    page = 0, will return 1-10 movies
    """

    def get(self, request):
        page = request.GET.get('page', None)
        if page is None:
            page = 0
        page = int(page)
        start = page * 10
        end = start + 10
        """
        prefetch_related helps to load more than 1 objects single database hit
        solves the n+1 issue
        """
        movies = Movies.objects.prefetch_related('genre').all()[start:end]
        serializer = MoviesSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetMovie(APIView):
    """
    This api accepts pk as input (url parameter) and will return matched object or 404
    """

    def get(self, request, id_pk):
        try:
            movie = Movies.objects.get(pk=id_pk)
            serializer = MoviesSerializer(movie)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Movies.DoesNotExist:
            raise Http404


class CreateMovie(APIView):
    """
    Use this api to create new movie.
    Auth token(Admin) is required for this api.
    With (permissions.IsAdminUser) Only admin have access to this api.
    
    parameters:

    post data
    name -> str
    popularity-> float
    director-> str
    imdb_score -> float
    genre -> [pk -> int]

    """
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request):
        genres = request.data.pop('genre')
        movie = Movies(**request.data)

        movie.save()
        for genre in genres:
            try:
                movie.genre.add(Genre.objects.get(pk=genre))
            except Exception as ex:
                print(type(ex).__name__)

            serializer = MoviesSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateMovie(APIView):
    """
    Use this api to update exiting movie.
    Auth token(Admin) is required for this api.
    With (permissions.IsAdminUser) Only admin have access to this api.
    
    parameters:
    pk(id) in url parameter
    
    post data
    name -> str
    popularity-> float
    director-> str
    imdb_score -> float
    genre -> [pk -> int]


    [issue]
    It will append new values(Distinct values) and will remove old ones.
    
    """

    permission_classes = (permissions.IsAdminUser,)

    def put(self, request, id_pk):
        genres = request.data.pop('genre')

        # movie, updated = Movies.objects.update_or_create(
        #     pk=id_pk,
        #     defaults=request.data,
        # )

        try:
            movie = Movies.objects.get(pk=id_pk)
            movie.name = request.data['name']
            movie.popularity = request.data['popularity']
            movie.director = request.data['director']
            movie.imdb_score = request.data['imdb_score']

            movie.save()
        except Exception as ex:
            print(type(ex).__name__)
            raise Http404

        for genre in genres:
            try:
                movie.genre.add(Genre.objects.get(pk=genre))
            except Exception as ex:
                print(type(ex).__name__)

            serializer = MoviesSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteMovie(APIView):
    """
    Use this api to delete exiting movie.
    Auth token(Admin) is required for this api.
    With (permissions.IsAdminUser) Only admin have access to this api.
    
    parameters:
    pk(id) in url parameter
    
    """

    permission_classes = (permissions.IsAdminUser,)

    def delete(self, request, id_pk):
        try:
            movie = Movies.objects.get(pk=id_pk)
            movie.delete()
            return Response(status=status.HTTP_200_OK)
        except Movies.DoesNotExist:
            raise Http404


class SearchMovie(APIView):
    """
    This api accepts query as url parameter
    can be string or float

    depending on wheather it is string or float filter query will make create different filters.
    """

    def get(self, request, query):
        movies = Movies.objects.prefetch_related('genre')
        try:
            query = float(query)
            movies = movies.filter(Q(popularity=query) | Q(imdb_score=query))
        except Exception as ex:
            print(type(ex).__name__)
            """
            iexact will look for exact match but case insensitive
            icontains will look for give string is substring of value or not
            """
            movies = movies.filter(
                Q(name__iexact=query) | Q(director__iexact=query)
                | Q(name__icontains=query) | Q(director__icontains=query)
                | Q(genre__name__icontains=query)
                | Q(genre__name__icontains=query))
            # genre__name this will span the filter query accross the relation

        serializer = MoviesSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
