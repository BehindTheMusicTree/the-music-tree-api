from rest_framework import serializers

from api.model.play.Fields import Fields
from api.model.play.Play import Play


class PlayModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Play
        fields = [Fields.USER, Fields.CONTENT_OBJECT_TYPE, Fields.CONTENT_PK]
