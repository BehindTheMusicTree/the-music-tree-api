from rest_framework import serializers

from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from bodzify_api.serializer.schema.playlist.base.output.Fields import Fields as AvailableFields


class Fields:
    UUID = AvailableFields.UUID
    NAME = AvailableFields.NAME


class BasePlaylistMinimumSerializer(serializers.ModelSerializer):

    class Meta:
        model = BasePlaylist
        fields = [Fields.UUID,
                  Fields.NAME]
