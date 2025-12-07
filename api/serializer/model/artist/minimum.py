from rest_framework import serializers

from api.model.artist.Artist import Artist
from api.serializer.AppInputSerializer import AppInputSerializer
from api.serializer.model.album.Fields import Fields as AvailableFields


class Fields:
    UUID = AvailableFields.UUID
    NAME = AvailableFields.NAME_PUBLIC


class ArtistMinimumSerializer(AppInputSerializer, serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = [Fields.UUID, Fields.NAME]
