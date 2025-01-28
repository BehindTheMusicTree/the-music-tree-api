
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from bodzify_api import settings
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
            raise ValidationError({ModelFields.NAME_PUBLIC: "already exists"})
        return super().validate(data)
