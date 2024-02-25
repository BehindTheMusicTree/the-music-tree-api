#!/usr/bin/env python

from django.http import QueryDict
from bodzify_api.serializer.playlist.simple.input.model.SimplePlaylistSaveModelSerializer \
    import SimplePlaylistSaveModelSerializer
from bodzify_api.serializer.playlist.simple.input.schema.SimplePlaylistPostSchemaSerializer \
    import SimplePlaylistPostSchemaSerializer
from bodzify_api.service.Service import Service
from rest_framework.serializers import Serializer


class SimplePlaylistService(Service):

    def _get_post_schema_serializer(self, post_schema_data: QueryDict) -> Serializer:
        return SimplePlaylistPostSchemaSerializer(data=post_schema_data)  # type: ignore

    def _get_put_schema_serializer(self, old_instance, put_schema_data: QueryDict) -> Serializer:
        raise NotImplementedError("You should implement this method in a subclass")

    def _get_save_model_serializer(self, old_instance, save_model_data: QueryDict, partial: bool) -> Serializer:
        return SimplePlaylistSaveModelSerializer(data=save_model_data)  # type: ignore

    def _get_save_schema_data_from_post_schema_data(self, post_schema_data: QueryDict) -> QueryDict:
        return post_schema_data

    def _get_save_model_data_from_save_schema_data(self, user, save_schema_data: QueryDict) -> QueryDict:
        return save_schema_data

    def _get_detailed_serializer(self, instance):
        raise NotImplementedError("You should implement this method in a subclass")
