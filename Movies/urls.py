from django.urls import path

from .views import (
    LoadJson,
    GetMovies,
    CreateMovie,
    UpdateMovie,
    DeleteMovie,
    SearchMovie,
    GetMovie,
)

urlpatterns = [
    path('', LoadJson.as_view()),
    path('list/', GetMovies.as_view()),
    path('create/', CreateMovie.as_view()),
    path('one/<int:id_pk>/', GetMovie.as_view()),
    path('update/<int:id_pk>/', UpdateMovie.as_view()),
    path('delete/<int:id_pk>/', DeleteMovie.as_view()),
    path('search/<str:query>/', SearchMovie.as_view()),
]
