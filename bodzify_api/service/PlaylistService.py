#!/usr/bin/env python

from django.contrib.auth.models import User
from django.http import QueryDict
from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.serializer.playlist.simple.input.model.SimplePlaylistPostModelSerializer import SimplePlaylistPostModelSerializer
from bodzify_api.serializer.playlist.simple.input.schema.SimplePlaylistPostSchemaSerializer \
    import SimplePlaylistPostSchemaSerializer
from bodzify_api.service.Service import Service


class PlaylistService(Service):

    def create_simple_playlist(self, user: User, data: QueryDict) -> SimplePlaylist:
        serializer = SimplePlaylistPostSchemaSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        save_model_data = data.copy()
        save_model_data[PLAYLIST_ATTRIBUTES_LABEL.USER] = user.id
        save_serializer = SimplePlaylistPostModelSerializer(data=save_model_data)
        save_serializer.is_valid(raise_exception=True)
        return save_serializer.save()
