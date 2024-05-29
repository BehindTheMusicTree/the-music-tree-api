#!/usr/bin/env python

from bodzify_api.serializer.playlist.children.simple.input.model \
    import SimplePlaylistModelSerializer
from bodzify_api.service.Service import Service


class PlaylistService(Service):

    def _get_save_model_serializer(self, old_instance, save_model_data: dict, partial: bool):
        return SimplePlaylistModelSerializer(data=save_model_data)
