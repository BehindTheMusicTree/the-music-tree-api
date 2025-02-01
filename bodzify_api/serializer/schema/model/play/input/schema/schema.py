from rest_framework import serializers

from bodzify_api.model.play.Play import Play, Fields as ModelFields
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.utils.validation_error_utils import raise_validation_error
from bodzify_api.view.error.ValidationResponseCode import ValidationResponseCode


class Fields:
    CONTENT_OBJECT_UUID = ModelFields.CONTENT_OBJECT + '_uuid'


class PlaySchemaSerializer(serializers.ModelSerializer):
    content_object_uuid = serializers.UUIDField()

    class Meta:
        model = Play
        fields = [Fields.CONTENT_OBJECT_UUID]

    def validate_content_object_uuid(self, object_pk):
        user = self.context['request'].user
        if not Playlist.objects.filter(user=user, uuid=object_pk).exists() \
                and not LibraryTrack.objects.filter(user=user, uuid=object_pk).exists():
            raise_validation_error(
                message='Object with this ID does not exist or does not belong to the user',
                code=ValidationResponseCode.FIELD_RESOURCE_NOT_OWNED.value,
                field=Fields.CONTENT_OBJECT_UUID
            )
        return object_pk
