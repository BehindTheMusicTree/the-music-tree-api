from rest_framework import serializers

from api.model.track.Track import Track
from api.serializer.model.artist.minimum import ArtistMinimumSerializer

from .Fields import Fields


class TrackMinimumSerializer(serializers.ModelSerializer):
    artists = ArtistMinimumSerializer(many=True)

    class Meta:
        model = Track
        fields = [Fields.UUID,
                  Fields.TITLE,
                  Fields.ARTISTS]
