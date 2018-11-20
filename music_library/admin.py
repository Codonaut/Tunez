from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from music_library.models import Song, Artist, Album, Library


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    fields = ('name', 'album')
    list_display = ('name', 'album')

    class Meta:
    	model = Song


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
	fields = ('name',)
	list_display = ('name',)

	class Meta:
		model = Artist


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
	fields = ('name', 'artist', 'release_year')
	list_display = ('name', 'artist', 'release_year')

	class Meta:
		model = Album


class LibraryInline(admin.StackedInline):
    model = Library
    verbose_name_plural = 'Library'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    """
    User a custom UserAdmin so we can edit a user's songs.
    """
    inlines = (LibraryInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)