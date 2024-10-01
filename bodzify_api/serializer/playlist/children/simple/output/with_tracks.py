#!/usr/bin/env python

from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.serializer.playlist.children.child \
    import ChildPlaylistSerializer, Fields as ChildPlaylistFields
from bodzify_api.serializer.playlist_lib_track_relation.output.without_playlist \
    import PlaylistLibTrackRelationWithoutPlaylist
from bodzify_api.model.playlist.BasePlaylist import ForeignModelRelationsStr as PLAYLIST_FOREIGN_MODEL_RELATIONS_STR
from rest_framework import serializers


class Fields:
    UUID = ChildPlaylistFields.UUID
    NAME = ChildPlaylistFields.NAME
    CREATED_ON = ChildPlaylistFields.CREATED_ON
    LIB_TRACKS = ChildPlaylistFields.LIB_TRACKS
    LIB_TRACKS_COUNT = ChildPlaylistFields.LIB_TRACKS_COUNT


class SimplePlaylistWithTracksSerializer(ChildPlaylistSerializer):
    name = serializers.CharField()  # Overriding the name field of the parent class
    library_tracks = PlaylistLibTrackRelationWithoutPlaylist(
        source=PLAYLIST_FOREIGN_MODEL_RELATIONS_STR.PLAYLIST_LIB_TRACK_RELATIONS, many=True)

    class Meta:
        model = SimplePlaylist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.CREATED_ON,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.LIB_TRACKS]
