

from rest_framework.exceptions import ValidationError

from bodzify_api.model.playlist.children.ManualPlaylist import ManualPlaylist
from bodzify_api.serializer.schema.endpoint import InputEndpointSerializer
from bodzify_api.serializer.schema.playlist.children.simple.input.schema \
    import Fields as SaveSchemaFields, ManualPlaylistSchemaSerializer


class ManualPlaylistInputEndpointSerializer(ManualPlaylistSchemaSerializer, InputEndpointSerializer):

    class Meta:
        model = ManualPlaylist
        fields = [SaveSchemaFields.NAME]

    def validate(self, data):
        user = self.context['request'].user
        name = data.get(SaveSchemaFields.NAME)
        if ManualPlaylist.objects.filter(user=user, name=name).exists():
            raise ValidationError({SaveSchemaFields.NAME: "already exists"})
        return super().validate(data)
