from rest_framework import serializers

from bodzify_api.model.play.Play import Play, Fields as ModelFields
from bodzify_api.serializer.field.foreign_key.TrackablePlayCountUuidField import TrackablePlayCountUuidField


class Fields:
    CONTENT_OBJECT_UUID = ModelFields.CONTENT_OBJECT + '_uuid'


class PlaySchemaSerializer(serializers.ModelSerializer):
    content_object_uuid = TrackablePlayCountUuidField()

    class Meta:
        model = Play
        fields = [Fields.CONTENT_OBJECT_UUID]
