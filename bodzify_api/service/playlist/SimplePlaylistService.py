#!/usr/bin/env python

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.serializer.playlist.children.simple.input.SimplePlaylistSaveModelSerializer \
    import SimplePlaylistSaveModelSerializer, FIELDS as SAVE_MODEL_FIELDS
from bodzify_api.serializer.playlist.children.simple.input.schema.SimplePlaylistInputEndpointSerializer \
    import SimplePlaylistInputEndpointSerializer
from bodzify_api.serializer.playlist.children.simple.input.schema.SimplePlaylistSaveSchemaSerializer \
    import SimplePlaylistSaveSchemaSerializer
from bodzify_api.serializer.playlist.mother.input.PlaylistSaveModelSerializer import PlaylistSaveModelSerializer
from bodzify_api.service.Service import Service


class SimplePlaylistService(Service):

    def _get_post_serializer(self, post_data: dict):
        return SimplePlaylistInputEndpointSerializer(data=post_data)

    def _get_put_serializer(self, old_instance, put_data: dict):
        return SimplePlaylistInputEndpointSerializer(data=put_data)

    def _get_save_schema_serializer(self, old_instance, save_schema_data: dict, request):
        return SimplePlaylistSaveSchemaSerializer(data=save_schema_data)

    def _get_save_model_serializer(self, old_instance, save_model_data: dict, partial: bool):
        return SimplePlaylistSaveModelSerializer(instance=old_instance, data=save_model_data, partial=True)

    def _get_save_schema_data_from_post_data(self, post_data: dict) -> dict:
        return post_data

    def _get_save_schema_data_from_put_data(self, put_data: dict, old_instance=None) -> dict:
        return put_data

    def _get_save_model_data_from_save_schema_data_not_including_user_field(
            self, user, save_schema_data: dict, old_instance) -> dict:
        if old_instance is None:
            playlist_uuid = Playlist.objects.create(user=user).uuid
        else:
            playlist_uuid = old_instance.playlist.uuid

        simple_playlist_model_data = dict()
        simple_playlist_model_data[SAVE_MODEL_FIELDS.PLAYLIST] = playlist_uuid

        return Service._get_dict1_overriden_with_dict2_for_each_key_provided_in_dict2(
            dict1=simple_playlist_model_data,
            dict2=save_schema_data,
            keys=[SAVE_MODEL_FIELDS.NAME])
