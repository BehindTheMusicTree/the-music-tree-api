#!/usr/bin/env python

from django.contrib.auth.models import User

from bodzify_api.serializer.album.detailed import AlbumDetailedSerializer
from bodzify_api.service.Service import Service


class AlbumService(Service):

    def _get_detailed_serializer(self, instance) -> AlbumDetailedSerializer:
        return AlbumDetailedSerializer(instance=instance)  # type: ignore

    def delete(self, user: User, instance):
        instance.delete_with_tracks_and_eventually_artists()
