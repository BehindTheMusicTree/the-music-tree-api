
from multiprocessing import context
from rest_framework.request import Request

from bodzify_api.serializer.schema.playlist.children.simple.input.endpoint import ManualPlaylistInputEndpointSerializer
from bodzify_api.serializer.schema.playlist.children.simple.input.model import ManualPlaylistModelSerializer
from bodzify_api.serializer.schema.playlist.children.simple.input.schema import ManualPlaylistSchemaSerializer
from bodzify_api.service.Service import Service


class ManualPlaylistService(Service):

    def _get_schema_serializer(self, oldinstance, schema_data: dict, request: Request):
        return ManualPlaylistSchemaSerializer(data=schema_data, context={'request': request})

    def _get_model_serializer(self, oldinstance, model_data: dict, partial: bool, request: Request):
        return ManualPlaylistModelSerializer(instance=oldinstance,
                                             data=model_data,
                                             partial=partial,
                                             context={'request': request})

    def _get_schema_data_from_post_data(self, post_data: dict) -> dict:
        return post_data

    def _get_schema_data_from_put_data(self, put_data: dict, oldinstance=None) -> dict:
        return put_data

    def _get_model_data_from_schema_data_not_including_user_field(
            self, user, schema_data: dict, oldinstance) -> dict:
        return schema_data
