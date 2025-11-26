from django.shortcuts import render, get_object_or_404
from django.utils import timezone


from .models import Movie
from shows.models import Showtime


# Create your views here.
def MovieList(request):
    now = timezone.now()
    movies = Movie.objects.filter(showtime__start_time__gt=now).distinct()

    return render(request, "movie_list.html", {"movies": movies})


def MovieDetail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    # get the showtimes for this movie that are in the future
    current_time = Showtime.objects.filter(
        movie=movie, start_time__gte=timezone.now()
    ).order_by("start_time")

    context = {"movie": movie, "showtimes": current_time}

    return render(request, "movie_detail.html", context)
