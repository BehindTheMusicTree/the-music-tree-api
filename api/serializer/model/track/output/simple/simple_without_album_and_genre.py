
from rest_framework import serializers

from api.model.track.Track import Track
from api.serializer.AppInputSerializer import AppInputSerializer
from api.serializer.model.artist.minimum import ArtistMinimumSerializer
from api.serializer.model.track.output.simple.Fields import Fields as SimpleFields


class Fields:
    UUID = SimpleFields.UUID
    TITLE = SimpleFields.TITLE
    ARTISTS = SimpleFields.ARTISTS
    RATING = SimpleFields.RATING
    LANGUAGE = SimpleFields.LANGUAGE
    PLAY_COUNT = SimpleFields.PLAY_COUNT


class TrackWithoutAlbumPlaylistGenreSerializer(AppInputSerializer, serializers.ModelSerializer):
    artists = ArtistMinimumSerializer(many=True)

    class Meta:
        model = Track
        fields = [Fields.UUID,
                  Fields.TITLE,
                  Fields.ARTISTS,
                  Fields.RATING,
                  Fields.LANGUAGE,
                  Fields.PLAY_COUNT,]

