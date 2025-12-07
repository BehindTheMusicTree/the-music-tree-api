
from rest_framework import serializers

from api.model.uploaded_track.UploadedTrack import UploadedTrack
from api.serializer.model.artist.minimum import ArtistMinimumSerializer
from api.serializer.model.criteria.output.minimum import CriteriaMinimumSerializer

from .Fields import Fields as SimpleFields


class Fields:
    UUID = SimpleFields.UUID
    TITLE = SimpleFields.TITLE
    ARTISTS = SimpleFields.ARTISTS
    TRACK_NUMBER = SimpleFields.TRACK_NUMBER
    GENRE = SimpleFields.GENRE
    RATING = SimpleFields.RATING
    LANGUAGE = SimpleFields.LANGUAGE
    PLAY_COUNT = SimpleFields.PLAY_COUNT


class UploadedTrackSimpleWithoutAlbumWithPositionInAlbumSerializer(serializers.ModelSerializer):
    genre = CriteriaMinimumSerializer()
    artists = ArtistMinimumSerializer(many=True)

    class Meta:
        model = UploadedTrack
        fields = [Fields.UUID,
                  Fields.TITLE,
                  Fields.ARTISTS,
                  Fields.TRACK_NUMBER,
                  Fields.GENRE,
                  Fields.RATING,
                  Fields.LANGUAGE,
                  Fields.PLAY_COUNT]
