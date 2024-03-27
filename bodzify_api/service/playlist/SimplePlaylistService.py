#!/usr/bin/env python

from django.http import QueryDict
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

    def _get_post_schema_serializer(self, post_schema_data: QueryDict):
        return SimplePlaylistInputEndpointSerializer(data=post_schema_data)

    def _get_put_schema_serializer(self, old_instance, put_schema_data: QueryDict):
        return SimplePlaylistInputEndpointSerializer(data=put_schema_data)

    def _get_save_schema_serializer(self, old_instance, save_schema_data: QueryDict, request):
        return SimplePlaylistSaveSchemaSerializer(data=save_schema_data)

    def _get_save_model_serializer(self, old_instance, save_model_data: QueryDict, partial: bool):
        return SimplePlaylistSaveModelSerializer(instance=old_instance, data=save_model_data, partial=True)

    def _get_save_schema_data_from_post_schema_data(self, post_schema_data: QueryDict) -> QueryDict:
        return post_schema_data

    def _get_save_schema_data_from_put_schema_data(self, put_schema_data: QueryDict, old_instance=None) -> QueryDict:
        return put_schema_data

    def _get_save_model_data_from_save_schema_data_not_including_user_field(
            self, user, save_schema_data: QueryDict, old_instance) -> QueryDict:
        if old_instance is None:
            playlist_uuid = Playlist.objects.create(user=user).uuid
        else:
            playlist_uuid = old_instance.playlist.uuid

        simple_playlist_model_data = QueryDict(mutable=True)
        simple_playlist_model_data[SAVE_MODEL_FIELDS.PLAYLIST] = playlist_uuid

        return Service._get_dict1_overriden_with_dict2_for_each_key_provided_in_dict2(
            dict1=simple_playlist_model_data,
            dict2=save_schema_data,
            keys=[SAVE_MODEL_FIELDS.NAME])
