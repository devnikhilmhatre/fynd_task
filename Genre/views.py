from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Genre
from .serializers import GenreSerializer
from django.http import Http404


class GetGenres(APIView):
    """
    This api will return all Genre's (Pagination is not implemented)
    """

    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetGenre(APIView):
    """
    This api accepts pk as input (url parameter) and will return matched object or 404
    """

    def get(self, request, id_pk):
        try:
            genre = Genre.objects.get(pk=id_pk)
            serializer = GenreSerializer(genre)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Genre.DoesNotExist:
            raise Http404


class CreateGenre(APIView):
    """
    Use this api to create new genre.
    Auth token(Admin) is required for this api.
    With (permissions.IsAdminUser) Only admin have access to this api.
    
    parameters:

    post data
    name -> str

    """

    permission_classes = (permissions.IsAdminUser,)

    def post(self, request):
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateGenre(APIView):
    """
    Use this api to update exiting genre.
    Auth token(Admin) is required for this api.
    With (permissions.IsAdminUser) Only admin have access to this api.
    
    parameters:
    pk(id) in url parameter
    
    post data
    name -> str
    
    """

    permission_classes = (permissions.IsAdminUser,)

    def put(self, request, id_pk):
        try:
            genre = Genre.objects.get(pk=id_pk)
        except Genre.DoesNotExist:
            raise Http404

        serializer = GenreSerializer(genre, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DeleteGenre(APIView):
    """
    Use this api to delete exiting genre.
    Auth token(Admin) is required for this api.
    With (permissions.IsAdminUser) Only admin have access to this api.
    
    parameters:
    pk(id) in url parameter
    
    """
    permission_classes = (permissions.IsAdminUser,)

    def delete(self, request, id_pk):
        try:
            genre = Genre.objects.get(pk=id_pk)
            genre.delete()
            return Response(status=status.HTTP_200_OK)
        except Genre.DoesNotExist:
            raise Http404