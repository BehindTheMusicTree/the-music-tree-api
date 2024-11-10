
from rest_framework import serializers

from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.serializer.schema.artist.minimum import ArtistMinimumSerializer
from bodzify_api.serializer.schema.criteria.output.minimum import CriteriaMinimumSerializer
from bodzify_api.serializer.schema.lib_track.output.simple.Fields import Fields as SimpleFields


class Fields:
    UUID = SimpleFields.UUID
    TITLE = SimpleFields.TITLE
    ARTISTS = SimpleFields.ARTISTS
    POSITION_IN_ALBUM = SimpleFields.POSITION_IN_ALBUM
    GENRE = SimpleFields.GENRE
    RATING = SimpleFields.RATING
    LANGUAGE = SimpleFields.LANGUAGE


class LibTrackSimpleWithoutAlbumWithPositionInAlbumSerializer(serializers.ModelSerializer):
    genre = CriteriaMinimumSerializer()
    artists = ArtistMinimumSerializer(many=True)

    class Meta:
        model = LibraryTrack
        fields = [Fields.POSITION_IN_ALBUM,
                  Fields.UUID,
                  Fields.TITLE,
                  Fields.ARTISTS,
                  Fields.GENRE,
                  Fields.RATING,
                  Fields.LANGUAGE,]
