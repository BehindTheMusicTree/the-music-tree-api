
from rest_framework import serializers

from bodzify_api.model.artist.Artist import Artist
from bodzify_api.serializer.schema.album.fields import Fields as AvailableFields


class Fields:
    UUID = AvailableFields.UUID
    NAME = AvailableFields.NAME


class ArtistMinimumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = [Fields.UUID, Fields.NAME]
