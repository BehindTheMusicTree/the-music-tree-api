
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from bodzify_api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from bodzify_api.serializer.AppValidationSerializer import AppValidationSerializer
from bodzify_api.serializer.schema.model.playlist.children.manual.input.schema \
    import Fields as SaveSchemaFields


class ManualPlaylistInputSerializer(AppValidationSerializer, serializers.ModelSerializer):
    class Meta:
        model = ManualPlaylist
        fields = [SaveSchemaFields.NAME]

    def validate(self, data):
        user = self.context['request'].user
        name = data.get(SaveSchemaFields.NAME)
        if ManualPlaylist.objects.filter(user=user, name=name).exists():
            raise ValidationError({SaveSchemaFields.NAME: "already exists"})
        return super().validate(data)
