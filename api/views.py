from django.contrib.auth.models import User
from django import http
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import generics, mixins, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from music_library.models import Song, Library
from music_library.serializers import SongSerializer



class SongList(generics.ListAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('name', 'album__name', 'album__release_year', 'album__artist__name')
    search_fields = filter_fields
    ordering_fields = filter_fields


class SongDetail(generics.RetrieveAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class UserSongList(generics.ListAPIView):
    serializer_class = SongSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('name', 'album__name', 'album__release_year', 'album__artist__name')
    search_fields = filter_fields
    ordering_fields = filter_fields

    def get_queryset(self):
        return Song.objects.filter(users=self.request.user)

    def patch(self, request, *args, **kwargs):
        """ Accept list of songs in 'songs' field.  The only required field is 'id'. """
        status_code = status.HTTP_200_OK
        user = request.user
        if 'songs' in request.data:
            for s in request.data['songs']:
                Library.objects.update_or_create(user=user, song_id=s['id'])
            status_code = status.HTTP_202_ACCEPTED
        return Response(SongSerializer(self.get_queryset(), many=True).data, status=status_code)

    def delete(self, request, *args, **kwargs):
        """
        Accept list of songs in 'songs' field.  The only required field is 'id'.
        Note: Accepting a body in a DELETE request is a bit weird.  Another option for song deletion
        would be to accept a PATCH request at /api/library/delete/.
        """
        data = request.data
        if 'songs' in request.data:
            song_ids = [s['id'] for s in request.data['songs']]
            Library.objects.filter(user=request.user, song_id__in=song_ids).delete()
        return Response(SongSerializer(self.get_queryset(), many=True).data, status=status.HTTP_202_ACCEPTED)

