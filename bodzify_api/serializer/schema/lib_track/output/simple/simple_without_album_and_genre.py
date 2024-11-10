
from rest_framework import serializers

from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.serializer.schema.artist.minimum import ArtistMinimumSerializer
from bodzify_api.serializer.schema.lib_track.output.simple.Fields import Fields as SimpleFields


class Fields:
    UUID = SimpleFields.UUID
    TITLE = SimpleFields.TITLE
    ARTISTS = SimpleFields.ARTISTS
    RATING = SimpleFields.RATING
    LANGUAGE = SimpleFields.LANGUAGE


class LibTrackWithoutAlbumPlaylistGenreSerializer(serializers.ModelSerializer):
    artists = ArtistMinimumSerializer(many=True)

    class Meta:
        model = LibraryTrack
        fields = [Fields.UUID,
                  Fields.TITLE,
                  Fields.ARTISTS,
                  Fields.RATING,
                  Fields.LANGUAGE]
