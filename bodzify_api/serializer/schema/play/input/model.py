
from rest_framework import serializers

from bodzify_api.model.Play import Fields, Play


class Fields:
    USER = Fields.USER
    CONTENT_TYPE = Fields.CONTENT_TYPE
    OBJECT_UUID = Fields.OBJECT_UUID


class PlayModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Play
        fields = [Fields.USER, Fields.CONTENT_TYPE, Fields.OBJECT_UUID]
