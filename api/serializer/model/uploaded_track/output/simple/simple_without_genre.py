
from rest_framework import serializers

from api.model.uploaded_track.UploadedTrack import UploadedTrack
from api.serializer.model.album.minimum import AlbumMinimumSerializer
from api.serializer.model.artist.minimum import ArtistMinimumSerializer
from api.serializer.model.uploaded_track.output.simple.Fields import Fields as SimpleFields


class Fields:
    UUID = SimpleFields.UUID
    TITLE = SimpleFields.TITLE
    ARTISTS = SimpleFields.ARTISTS
    ALBUM = SimpleFields.ALBUM
    GENRE = SimpleFields.GENRE
    RATING = SimpleFields.RATING
    LANGUAGE = SimpleFields.LANGUAGE
    PLAY_COUNT = SimpleFields.PLAY_COUNT


class UploadedTrackSimpleWithoutGenreSerializer(serializers.ModelSerializer):
    artists = ArtistMinimumSerializer(many=True)
    album = AlbumMinimumSerializer()

    class Meta:
        model = UploadedTrack
        fields = [Fields.UUID,
                  Fields.TITLE,
                  Fields.ARTISTS,
                  Fields.ALBUM,
                  Fields.RATING,
                  Fields.LANGUAGE,
                  Fields.PLAY_COUNT]
