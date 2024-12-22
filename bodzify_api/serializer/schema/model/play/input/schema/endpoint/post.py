from bodzify_api.model.play.Play import Play
from bodzify_api.serializer.field.UserContentObjectUuidField import UserContentObjectUuidField
from bodzify_api.serializer.schema.base_input.AppInputModelSerializer import AppInputModelSerializer
from .Fields import Fields


class PlayPostSerializer(AppInputModelSerializer):
    content_object_uuid = UserContentObjectUuidField()

    class Meta:
        model = Play
        fields = [Fields.CONTENT_OBJECT_UUID]
