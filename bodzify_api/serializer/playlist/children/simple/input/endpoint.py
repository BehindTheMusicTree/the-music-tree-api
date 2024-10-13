
#!/usr/bin/env python

from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.serializer.endpoint import InputEndpointSerializer
from bodzify_api.serializer.playlist.children.simple.input.schema import \
    Fields as SaveSchemaFields
from bodzify_api.serializer.playlist.children.simple.input.schema import \
    SimplePlaylistSchemaSerializer


class SimplePlaylistInputEndpointSerializer(SimplePlaylistSchemaSerializer, InputEndpointSerializer):

    class Meta:
        model = SimplePlaylist
        fields = [SaveSchemaFields.NAME]
