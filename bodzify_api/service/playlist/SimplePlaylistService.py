#!/usr/bin/env python

from django.http import QueryDict
from bodzify_api.serializer.playlist.input.PlaylistSaveModelSerializer import PlaylistSaveModelSerializer
from bodzify_api.serializer.playlist.simple.input.model.SimplePlaylistSaveModelSerializer \
    import SimplePlaylistSaveModelSerializer, FIELDS as SIMPLE_PLAYLIST_SAVE_MODEL_FIELDS
from bodzify_api.serializer.playlist.simple.input.schema.SimplePlaylistPostSchemaSerializer \
    import SimplePlaylistPostSchemaSerializer
from bodzify_api.serializer.playlist.input.PlaylistSaveModelSerializer import FIELDS as PLAYLIST_SAVE_MODEL_FIELDS
from bodzify_api.serializer.playlist.simple.input.schema.SimplePlaylistPutSchemaSerializer import SimplePlaylistPutSchemaSerializer
from bodzify_api.service.Service import Service
from rest_framework.serializers import Serializer


class SimplePlaylistService(Service):

    def _get_post_schema_serializer(self, post_schema_data: QueryDict) -> Serializer:
        return SimplePlaylistPostSchemaSerializer(data=post_schema_data)  # type: ignore

    def _get_put_schema_serializer(self, old_instance, put_schema_data: QueryDict) -> Serializer:
        return SimplePlaylistPutSchemaSerializer(data=put_schema_data)  # type: ignore

    def _get_save_model_serializer(self, old_instance, save_model_data: QueryDict, partial: bool) -> Serializer:
        return SimplePlaylistSaveModelSerializer(
            instance=old_instance, data=save_model_data, partial=True)  # type: ignore

    def _get_save_schema_data_from_post_schema_data(self, post_schema_data: QueryDict) -> QueryDict:
        return post_schema_data

    def _get_save_model_data_from_save_schema_data(self, user, save_schema_data: QueryDict, old_instance) -> QueryDict:
        if old_instance is None:
            playlist_save_model_data = QueryDict(mutable=True)
            playlist_save_model_data[PLAYLIST_SAVE_MODEL_FIELDS.USER] = user.id  # type: ignore
            playlist_save_model_serializer = PlaylistSaveModelSerializer(data=playlist_save_model_data)
            playlist_save_model_serializer.is_valid(raise_exception=True)
            playlist = playlist_save_model_serializer.save()
            playlist_uuid = playlist.uuid  # type: ignore
        else:
            playlist_uuid = old_instance.playlist.uuid

        simple_playlist_model_data = QueryDict(mutable=True)
        simple_playlist_model_data[SIMPLE_PLAYLIST_SAVE_MODEL_FIELDS.PLAYLIST] = playlist_uuid

        return Service._get_dict1_overriden_with_dict2_for_each_key_provided_in_dict2(
            dict1=simple_playlist_model_data,
            dict2=save_schema_data,
            keys=[SIMPLE_PLAYLIST_SAVE_MODEL_FIELDS.NAME])
