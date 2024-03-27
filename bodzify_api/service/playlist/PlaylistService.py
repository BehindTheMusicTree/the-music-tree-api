#!/usr/bin/env python

from bodzify_api.serializer.playlist.children.simple.input.SimplePlaylistSaveModelSerializer \
    import SimplePlaylistSaveModelSerializer
from bodzify_api.service.Service import Service


class PlaylistService(Service):

    def _get_save_model_serializer(self, old_instance, save_model_data: dict, partial: bool):
        return SimplePlaylistSaveModelSerializer(data=save_model_data)
