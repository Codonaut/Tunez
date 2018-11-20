from django.db import models
from django.contrib.auth.models import User


class Artist(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name


class Album(models.Model):
	name = models.CharField(max_length=255)
	artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
	release_year = models.IntegerField()

	def __str__(self):
		return self.name


class Song(models.Model):
	name = models.CharField(max_length=255)
	# We're assuming that every song is released on an album, and every album has one Artist.
	album = models.ForeignKey(Album, on_delete=models.CASCADE)
	# The users that have this song added to their library. Stored in many-to-many mapping table.
	users = models.ManyToManyField(User, through='Library', related_name='songs')

	def __str__(self):
		return self.name


class Library(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	song = models.ForeignKey(Song, on_delete=models.CASCADE)

	class Meta:
		unique_together = (('user', 'song'),)
