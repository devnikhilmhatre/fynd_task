from django.db import models
from Genre.models import Genre
# Create your models here.


class Movies(models.Model):
    name = models.CharField(max_length=120)
    popularity = models.FloatField()
    director = models.CharField(max_length=100)
    genre = models.ManyToManyField(Genre)
    imdb_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
