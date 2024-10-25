#!/usr/bin/env python

from bodzify_api.model.playlist.children.ManualPlaylist import Fields, ManualPlaylist
from bodzify_api.serializer.schema.playlist.children.model import ChildPlaylistModelSerializer


class Fields:
    NAME = Fields.NAME


class ManualPlaylistModelSerializer(ChildPlaylistModelSerializer):

    class Meta:
        model = ManualPlaylist
        fields = [Fields.NAME]
