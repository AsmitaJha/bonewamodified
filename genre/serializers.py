from rest_framework import serializers
from .models import Genre

class GenreSerializer(serializers.ModelSerializer):
    genres_list=serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = ["title","genres_list"]
        
    def get_genres_list(self, obj):
        return Genre.genres_list()