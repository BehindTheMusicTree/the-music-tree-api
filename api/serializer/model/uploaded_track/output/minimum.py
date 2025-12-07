from rest_framework import serializers

from api.model.uploaded_track.UploadedTrack import UploadedTrack
from api.serializer.model.artist.minimum import ArtistMinimumSerializer

from .Fields import Fields


class UploadedTrackMinimumSerializer(serializers.ModelSerializer):
    artists = ArtistMinimumSerializer(many=True)

    class Meta:
        model = UploadedTrack
        fields = [Fields.UUID,
                  Fields.TITLE,
                  Fields.ARTISTS]
