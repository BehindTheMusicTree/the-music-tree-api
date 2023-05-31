#!/usr/bin/env python

from django.contrib.auth.models import User
from django.http import QueryDict

from bodzify_api.serializer.playlist.input.SimplePlaylistPostSerializer import SimplePlaylistPostSerializer


class PlaylistService:

	def createSimplePlaylist(self, user: User, data: QueryDict):
		schemaSerializer = SimplePlaylistPostSerializer(data=data)
		schemaSerializer.is_valid(raise_exception=True)
		playlist = schemaSerializer.save()

		playlist.save()

		return playlist
