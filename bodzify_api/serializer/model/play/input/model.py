from rest_framework import serializers

from bodzify_api.model.play.Fields import Fields
from bodzify_api.model.play.Play import Play


class PlayModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Play
        fields = [Fields.USER, Fields.CONTENT_OBJECT_TYPE, Fields.CONTENT_PK]
