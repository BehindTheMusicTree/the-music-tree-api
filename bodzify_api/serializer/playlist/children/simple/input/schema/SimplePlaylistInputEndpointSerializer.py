
#!/usr/bin/env python

from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.serializer.InputEndpointSerializer import InputEndpointSerializer
from bodzify_api.serializer.playlist.children.simple.input.schema.SimplePlaylistSaveSchemaSerializer \
    import SimplePlaylistSaveSchemaSerializer, FIELDS as SAVE_SCHEMA_FIELDS


class SimplePlaylistInputEndpointSerializer(SimplePlaylistSaveSchemaSerializer, InputEndpointSerializer):

    class Meta:
        model = SimplePlaylist
        fields = [SAVE_SCHEMA_FIELDS.NAME]
