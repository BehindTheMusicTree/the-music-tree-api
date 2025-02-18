from rest_framework import serializers

from bodzify_api.model.play.Play import Play
from bodzify_api.model.play.Fields import Fields


class PlayModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Play
        fields = [Fields.USER, Fields.CONTENT_OBJECT_TYPE, Fields.CONTENT_PK]
