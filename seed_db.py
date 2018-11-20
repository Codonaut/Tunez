"""
Insert a little bit of artist/album/song data into the DB.
"""
from music_library.models import Artist, Album, Song


artists = {
	'Santana': [
		{
			'album': 'Abraxas',
			'songs': ['Oye Como Va', 'Black Magic Woman'],
			'release_year': 1970
		}
	],
	'Miles Davis': [
		{
			'album': 'Kind of Blue',
			'songs': ['So What', 'All Blues'],
			'release_year': 1959
		},
		{
			'album': 'In a Silent Way',
			'songs': ['In a Silent Way'],
			'release_year': 1969
		}
	],
	'Mitski': [
		{
			'album': 'Be the Cowboy',
			'songs': ['Nobody', 'Me and my Husband', 'Geyser'],
			'release_year': 2018
		},
		{
			'album': 'Bury Me at Makeout Creek',
			'release_year': 2014,
			'songs': ['Texas Reznikoff', 'Townie']
		}
	]
}

print('Seeding data...')

for artist_name, albums in artists.items():
	artist = Artist(name=artist_name)
	artist.save()
	for d in albums:
		album = Album(name=d['album'], release_year=d['release_year'], artist=artist)
		album.save()
		for song_name in d['songs']:
			Song(name=song_name, album=album).save()

print('Done.')
