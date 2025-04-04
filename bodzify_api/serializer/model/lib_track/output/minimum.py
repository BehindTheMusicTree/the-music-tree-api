from rest_framework import serializers

from bodzify_api.model.uploaded_track.UploadedTrack import UploadedTrack
from bodzify_api.serializer.model.artist.minimum import ArtistMinimumSerializer

from .Fields import Fields


class LibTrackMinimumSerializer(serializers.ModelSerializer):
    artists = ArtistMinimumSerializer(many=True)

    class Meta:
        model = UploadedTrack
        fields = [Fields.UUID,
                  Fields.TITLE,
                  Fields.ARTISTS]
