
from rest_framework import serializers

from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.serializer.model.album.minimum import AlbumMinimumSerializer
from bodzify_api.serializer.model.artist.minimum import ArtistMinimumSerializer
from bodzify_api.serializer.model.criteria.output.minimum import CriteriaMinimumSerializer
from bodzify_api.serializer.model.lib_track.output.simple.Fields import Fields as SimpleFields


class Fields:
    UUID = SimpleFields.UUID
    TITLE = SimpleFields.TITLE
    ARTISTS = SimpleFields.ARTISTS
    ALBUM = SimpleFields.ALBUM
    GENRE = SimpleFields.GENRE
    RATING = SimpleFields.RATING
    LANGUAGE = SimpleFields.LANGUAGE
    PLAY_COUNT = SimpleFields.PLAY_COUNT


class LibTrackSimpleWithoutPositionInAlbumSerializer(serializers.ModelSerializer):
    artists = ArtistMinimumSerializer(many=True)
    album = AlbumMinimumSerializer()
    genre = CriteriaMinimumSerializer()

    class Meta:
        model = LibraryTrack
        fields = [Fields.UUID,
                  Fields.TITLE,
                  Fields.ARTISTS,
                  Fields.ALBUM,
                  Fields.GENRE,
                  Fields.RATING,
                  Fields.LANGUAGE,
                  Fields.PLAY_COUNT]
