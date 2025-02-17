from rest_framework import serializers

from bodzify_api.model.play.Play import Play
from bodzify_api.serializer.AppValidationSerializer import AppValidationSerializer
from bodzify_api.serializer.field.foreign_key.UserContentObjectUuidField import UserContentObjectUuidField
from .Fields import Fields


class PlayPostSerializer(AppValidationSerializer, serializers.ModelSerializer):
    content_object_uuid = UserContentObjectUuidField()

    class Meta:
        model = Play
        fields = [Fields.CONTENT_OBJECT_UUID]
