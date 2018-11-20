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

Notes to the Reader
===================

* Normally I'd make sure I didn't have things like unused imports.  On this project I didn't.
* Normally I'd make sure the home page literally serves any purpose at all, and doesn't have broken links.

This is a silly take-home challenge.  It took me ~5 hours, even though I said I'd spend maximum 3.  How did I spend that time?  Well, spinning up a new project takes time, since that is such a small part of what I do as an engineer.  Then of course there was the time to bang around re-familiarizing myself with Django Rest Framework.  With all of that time I've created a just-barely-works API.  What does this show you guys?  Well, I know how to glue stuff together-- you can tell that much.  So your signal shows that I kind of know what I'm doing... and in order to generate that signal I spent 5 hours of my time.  In retrospect I wish I hadn't, and I'm a little annoyed that I did.  Expecting candidates to spend 5+ hours on a take-home challenge is completely unrealistic, especially when hiring in a tough (for employers) market like SF.

If I end up working with you guys then I will strongly push for removing (or heavily changing) this aspect of interviewing.