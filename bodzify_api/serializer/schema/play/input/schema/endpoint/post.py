
from bodzify_api.model.Play import Play, Fields as ModelFields
from bodzify_api.serializer.field.UserFilteredContentObjectUUIDField import UserFilteredPlayContentObjectUUIDField
from bodzify_api.serializer.schema.endpoint import InputEndpointSerializer


class Fields:
    CONTENT_OBJECT_UUID = ModelFields.CONTENT_OBJECT + '_uuid'


class PlayPostSerializer(InputEndpointSerializer):
    content_object_uuid = UserFilteredPlayContentObjectUUIDField()

    class Meta:
        model = Play
        fields = [Fields.CONTENT_OBJECT_UUID]
