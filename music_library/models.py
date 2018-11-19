from django.db import models
from django.contrib.auth.models import User


class Artist(models.Model):
	name = models.CharField(max_length=255)


class Album(models.Model):
	name = models.CharField(max_length=255)
	artist = models.ForeignKey(Artist, on_delete=models.CASCADE)


class Song(models.Model):
	name = models.CharField(max_length=255)
	# We're assuming that every song is released on an album, and every album has one Artist.
	album = models.ForeignKey(Album, on_delete=models.CASCADE)
	# The users that have this song added to their library.
	users = models.ManyToManyField(User)
