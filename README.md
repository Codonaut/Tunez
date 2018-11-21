Contributing
============

* Create virtualenv: `python3 -m venv .venv`
* Activate it: `source .venv/bin/activate`
* Install packages: `pip3 install -r requirements.txt`
* Run DB Migrations: `python3 manage.py migrate`
* Seed DB with some mock data: `python3 manage.py shell < seed_db.py`
* Create a super user to access admin site: `python3 manage.py createsuperuser`
* Run the server: `python3 manage.py runserver`

Notes
=====

* Unless otherwise stated, assume it isn't implemented.
* Multi-tenant app(though user creation is only done via command line). Login at /accounts/login.  Logout at /accounts/logout.  API authentication is done using session cookies.
* API for users to read Artists/Songs/Albums, and edit their own personal music library.
* Admin panel available at /admin. Useful for arbitrary CRUD on data.
* Small script to seed a local SQLite DB(make sure to run *after* performing DB migrations)

API
===

* To test API first login at /accounts/login.  Then, either browse the API in your browser(Django REST Framework creates an HTTP browsable API.  Just go to /api/songs!  It's kinda amazing.), or copy the session cookie and hit it with an HTTP client of your choice.
* API uses session auth.  A user cannot view the library of another user.
* Search by song name, album_name, artist_name, and album release year with the "search" query param
* Filter by name, album_name, artist_name, and album release year with query params e.g.
	* name=foo
	* album__name=foo
	* album__artist__name=foo
	* album__release_year=foo
* Order by name, album_name, artist_name, and album release year with the `ordering` query param.
	* reverse directio by prepending a minus e.g. `ordering=-album__artist__name` to sort in descending order by artist name


There is a read-only songs API allows listing of songs at /songs/, and song detail view at /songs/{song_id}.  
A song body looks like this: `{"id": 1, "name": "Oye Como Va", "album_name": "Abraxas", "artist_name": "Santana", "album_id": 1, "artist_id": 1}`.  I chose to have separate fields for album_name and album_id, and artist_name and artist_id.  album_name and artist_name are both redundant pieces of information, since (assuming the API is implemented...) with the ID of the album and the artist any caller/client can easily fetch the name.  But, the name is quite useful for display purposes so I decided to keep it in in order to make the API overall a bit easier to use.

The main songs API is read-only, and the hypothetical album and artist APIs would also be read-only.  This is because it seems like a bad idea to let arbitrary users be telling the system about new albums and artists.  That's a recipe for bad data!  Currently artists/albums/songs are added via the admin panel or by script.  As this amazing app evolves a more solid process will evolve to handle new songs(probably by integration with some canonical industry DB).

The /library/ endpoint is how user's interact with their own personal library.  A `GET` request to /library/ will return a list of all of the songs a user has added/starred/favorited/liked/whatever.  To add new songs to their Library a `PATCH` request should be sent to /library/ with a body containing a list of objects each containing a song ID(callers can send whole song objects-- the API just cares about the ID).  Each song sent in the `PATCH` body will be added to that user's library.  To delete songs from the library send the same kind of body to /library/, but send it as a `DELETE` request.  Sending a `DELETE` request with a body is a bit unconventional, but it seemed to make sense in this case.

Data Models
===========
The Artist, Album, and Song models are all pretty straightforward.  A song has an album, and an album has an artist.

The Library model is the more interesting one (by a bit).  It is a mapping table between Users and Songs, and it represents a user's Library.  In retrospect I would've named it UserSong(similar to the API view name) so I can avoid wonky code like `libraries = Library.objects.filter(user=request.user)`.  I think we can all agree `libraries` is a bad name here.  But, I don't feel like taking the time to go back.
