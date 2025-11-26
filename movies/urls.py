from django.urls import path

from .views import MovieList, MovieDetail

urlpatterns = [
    path('', MovieList, name='movie-list'),
    path('<int:movie_id>/', MovieDetail, name='movie-detail'),
]
