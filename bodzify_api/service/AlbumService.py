#!/usr/bin/env python

from bodzify_api.model.Album import Album
from bodzify_api.model.user.User import User

from bodzify_api.serializer.schema.album.detailed import AlbumDetailedSerializer
from bodzify_api.service.Service import Service


class AlbumService(Service):

    def _get_detailed_serializer_instance(self, instance) -> AlbumDetailedSerializer:
        return AlbumDetailedSerializer(instance=instance)  # type: ignore

    def delete(self, user: User, instance: Album):
        instance.delete_with_tracks_and_eventually_artists()
