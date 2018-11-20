from rest_framework import serializers
from .models import Artist, Album, Song


class SongSerializer(serializers.Serializer):
	id = serializers.IntegerField(read_only=True)
	name = serializers.CharField(read_only=True)
	album_name = serializers.StringRelatedField(source='album', read_only=True)
	artist_name = serializers.StringRelatedField(source='album.artist', read_only=True)
	album_id = serializers.PrimaryKeyRelatedField(source='album.id', read_only=True)
	artist_id = serializers.PrimaryKeyRelatedField(source='album.artist.id', read_only=True)
