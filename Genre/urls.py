from django.urls import path

from .views import (
    GetGenres,
    GetGenre,
    CreateGenre,
    UpdateGenre,
    DeleteGenre,
)

urlpatterns = [
    path('list/', GetGenres.as_view()),
    path('one/<int:id_pk>/', GetGenre.as_view()),
    path('create/', CreateGenre.as_view()),
    path('update/<int:id_pk>/', UpdateGenre.as_view()),
    path('delete/<int:id_pk>/', DeleteGenre.as_view()),
]
