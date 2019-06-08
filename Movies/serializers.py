from rest_framework.serializers import ModelSerializer
from .models import Movies
from Genre.serializers import GenreSerializer


class MoviesSerializer(ModelSerializer):
    """ 
    This helps you fetch all the data from related tables
    Removing this will only return pk for genre while fetching movies 
    """
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Movies
        fields = '__all__'
