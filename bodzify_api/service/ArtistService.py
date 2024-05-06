#!/usr/bin/env python


from django.contrib.auth.models import User

from bodzify_api.service.Service import Service


class ArtistService(Service):

    def delete(self, user: User, instance):
        instance.delete_with_albums_and_tracks()
