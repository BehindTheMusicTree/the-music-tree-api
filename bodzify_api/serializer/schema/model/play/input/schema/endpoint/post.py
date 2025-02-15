from bodzify_api.model.play.Play import Play
from bodzify_api.serializer.field.UserContentObjectUuidField import UserContentObjectUuidField
from bodzify_api.serializer.AppModelSerializer import AppModelSerializer
from .Fields import Fields


class PlayPostSerializer(AppModelSerializer):
    content_object_uuid = UserContentObjectUuidField()

    class Meta:
        model = Play
        fields = [Fields.CONTENT_OBJECT_UUID]
