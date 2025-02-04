
from rest_framework import serializers
from django.utils.translation import gettext as _
from bodzify_api import settings
from bodzify_api.utils.validation_error_utils import raise_validation_error
from bodzify_api.view.error.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from bodzify_api.model.playlist.children.manual.Fields import Fields as ModelFields
from bodzify_api.serializer.AppValidationSerializer import AppValidationSerializer


class ManualPlaylistInputSerializer(AppValidationSerializer, serializers.ModelSerializer):
    name = serializers.CharField(max_length=settings.MANUAL_PLAYLIST_NAME_LEN_MAX, allow_blank=False)

    class Meta:
        model = ManualPlaylist
        fields = [ModelFields.NAME_PUBLIC]

    def validate(self, data):
        user = self.context['request'].user
        name = data.get(ModelFields.NAME_PUBLIC)
        if ManualPlaylist.objects.filter(user=user, name=name).exists():
            raise_validation_error(
                message=_('A playlist with this name already exists'),
                code=FieldValidationErrorCode.FIELD_PLAYLIST_NAME_DUPLICATE.value,
                field=ModelFields.NAME_PUBLIC
            )
        return super().validate(data)
