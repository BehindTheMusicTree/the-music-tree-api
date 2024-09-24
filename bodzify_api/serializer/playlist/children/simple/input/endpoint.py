
#!/usr/bin/env python

from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.serializer.endpoint import InputEndpointSerializer
from bodzify_api.serializer.playlist.children.simple.input.schema \
    import SimplePlaylistSchemaSerializer, Fields as SAVE_SCHEMA_FIELDS


class SimplePlaylistInputEndpointSerializer(SimplePlaylistSchemaSerializer, InputEndpointSerializer):

    class Meta:
        model = SimplePlaylist
        fields = [SAVE_SCHEMA_FIELDS.NAME]
