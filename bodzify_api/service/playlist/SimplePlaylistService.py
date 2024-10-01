#!/usr/bin/env python

import re
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from bodzify_api.serializer.playlist.children.simple.input.model \
    import SimplePlaylistModelSerializer, Fields as SaveModelFields
from bodzify_api.serializer.playlist.children.simple.input.endpoint \
    import SimplePlaylistInputEndpointSerializer
from bodzify_api.serializer.playlist.children.simple.input.schema \
    import SimplePlaylistSchemaSerializer
from bodzify_api.service.Service import Service


class SimplePlaylistService(Service):

    def _get_post_serializer(self, post_data: dict):
        return SimplePlaylistInputEndpointSerializer(data=post_data)

    def _get_put_serializer(self, old_instance, put_data: dict):
        return SimplePlaylistInputEndpointSerializer(data=put_data)

    def _get_schema_serializer(self, old_instance, schema_data: dict, request):
        return SimplePlaylistSchemaSerializer(data=schema_data)

    def _get_model_serializer(self, old_instance, model_data: dict, partial: bool):
        return SimplePlaylistModelSerializer(instance=old_instance, data=model_data, partial=True)

    def _get_schema_data_from_post_data(self, post_data: dict) -> dict:
        return post_data

    def _get_schema_data_from_put_data(self, put_data: dict, old_instance=None) -> dict:
        return put_data

    def _get_model_data_from_schema_data_not_including_user_field(
            self, user, schema_data: dict, old_instance) -> dict:
        if old_instance is None:
            playlist_uuid = BasePlaylist.objects.create(user=user).uuid
        else:
            playlist_uuid = old_instance.base_playlist.uuid

        simple_playlist_model_data = dict()
        simple_playlist_model_data[SaveModelFields.BASE_PLAYLIST] = playlist_uuid

        Service._override_data1_with_data2_values_for_each_key_in_data2(
            data1=simple_playlist_model_data,
            data2=schema_data,
            keys=[SaveModelFields.NAME])

        return simple_playlist_model_data
