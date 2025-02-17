from rest_framework import serializers

from bodzify_api.model.artist.Artist import Artist
from bodzify_api.serializer.AppValidationSerializer import AppValidationSerializer
from bodzify_api.serializer.schema.model.album.Fields import Fields as AvailableFields


class Fields:
    UUID = AvailableFields.UUID
    NAME = AvailableFields.NAME


class ArtistMinimumSerializer(AppValidationSerializer, serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = [Fields.UUID, Fields.NAME]
