#!/usr/bin/env python

from django.http import QueryDict
from bodzify_api.serializer.playlist.children.simple.input.SimplePlaylistSaveModelSerializer \
    import SimplePlaylistSaveModelSerializer
from bodzify_api.service.Service import Service
from rest_framework.serializers import Serializer


class PlaylistService(Service):

    def _get_save_model_serializer(self, old_instance, save_model_data: QueryDict, partial: bool) -> Serializer:
        return SimplePlaylistSaveModelSerializer(data=save_model_data)  # type: ignore
