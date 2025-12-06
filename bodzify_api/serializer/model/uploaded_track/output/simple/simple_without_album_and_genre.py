
from rest_framework import serializers

from bodzify_api.model.uploaded_track.UploadedTrack import UploadedTrack
from bodzify_api.serializer.AppInputSerializer import AppInputSerializer
from bodzify_api.serializer.model.artist.minimum import ArtistMinimumSerializer
from bodzify_api.serializer.model.uploaded_track.output.simple.Fields import Fields as SimpleFields


class Fields:
    UUID = SimpleFields.UUID
    TITLE = SimpleFields.TITLE
    ARTISTS = SimpleFields.ARTISTS
    RATING = SimpleFields.RATING
    LANGUAGE = SimpleFields.LANGUAGE
    PLAY_COUNT = SimpleFields.PLAY_COUNT


class UploadedTrackWithoutAlbumPlaylistGenreSerializer(AppInputSerializer, serializers.ModelSerializer):
    artists = ArtistMinimumSerializer(many=True)

    class Meta:
        model = UploadedTrack
        fields = [Fields.UUID,
                  Fields.TITLE,
                  Fields.ARTISTS,
                  Fields.RATING,
                  Fields.LANGUAGE,
                  Fields.PLAY_COUNT,]
