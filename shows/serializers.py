from rest_framework.serializers import ModelSerializer


from .models import Showtime
from movies.serializers import MovieSerializer, ScreenReadSerializer

class ShowtimeSerializer(ModelSerializer):
    movie = MovieSerializer(read_only=True)
    screen = ScreenReadSerializer(read_only=True)
    
    class Meta:
        model = Showtime
        fields = ['id', 'movie', 'screen', 'start_time', 'end_time']
        
        
class CreateShowtimeSerializer(ModelSerializer):
    class Meta:
        model = Showtime
        fields = ['movie', 'screen', 'start_time']