#!/usr/bin/env python

from rest_framework.request import Request

from bodzify_api.serializer.schema.playlist.children.simple.input.model import ManualPlaylistModelSerializer
from bodzify_api.service.Service import Service


class PlaylistService(Service):

    def _get_model_serializer(self, oldinstance, model_data: dict, partial: bool, request: Request):
        return ManualPlaylistModelSerializer(data=model_data, partial=partial, context={'request': request})
