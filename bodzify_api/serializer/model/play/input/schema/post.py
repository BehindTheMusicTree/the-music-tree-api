from typing import Dict

from rest_framework import serializers

from bodzify_api.model.play.Play import Play
from bodzify_api.serializer.AppSerializer import AppSerializer
from bodzify_api.serializer.field.foreign_key.UserContentObjectUuidField import \
    PrivateContentUuidField

from .PostFields import Fields as PostFields
from .SchemaFields import Fields as SchemaFields


class PlayPostSerializer(AppSerializer, serializers.ModelSerializer):
    content = PrivateContentUuidField(write_only=True)

    class Meta:
        model = Play
        fields = [PostFields.CONTENT]

    def validate(self, attrs: Dict) -> Dict:
        content_data = attrs.pop(PostFields.CONTENT)
        attrs[SchemaFields.CONTENT_TYPE] = content_data[SchemaFields.CONTENT_TYPE]
        attrs[SchemaFields.CONTENT] = content_data[SchemaFields.CONTENT]
        return attrs
