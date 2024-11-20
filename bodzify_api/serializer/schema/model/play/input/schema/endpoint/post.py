from bodzify_api.model.play.Play import Play
from bodzify_api.serializer.field.UserFilteredContentObjectUUIDField import UserFilteredPlayContentObjectUUIDField
from bodzify_api.serializer.schema.base_input.BaseInputModelSerializer import BaseInputModelSerializer
from .Fields import Fields


class PlayPostSerializer(BaseInputModelSerializer):
    content_object_uuid = UserFilteredPlayContentObjectUUIDField()

    class Meta:
        model = Play
        fields = [Fields.CONTENT_OBJECT_UUID]
