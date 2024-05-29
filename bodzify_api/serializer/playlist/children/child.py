#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.playlist.children.CriteriaPlaylist import ATTRIBUTES_LABEL as CRITERIA_PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.model.playlist.BasePlaylist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.model.playlist.BasePlaylist import FOREIGN_MODEL_RELATIONS_STR as PLAYLIST_FOREIGN_MODEL_RELATIONS_STR
from bodzify_api.serializer.playlist.base.output.without_tracks \
    import BasePlaylistWithoutTracksSerializer
from bodzify_api.serializer.track.output.without_playlists_and_album \
    import LibTrackWithoutAlbumAndPlaylistSerializer


class FIELDS:
    UUID = PLAYLIST_ATTRIBUTES_LABEL.UUID
    NAME = CRITERIA_PLAYLIST_ATTRIBUTES_LABEL.NAME
    CREATED_ON = PLAYLIST_ATTRIBUTES_LABEL.CREATED_ON
    LIB_TRACKS_COUNT = PLAYLIST_ATTRIBUTES_LABEL.LIB_TRACKS_COUNT
    LIB_TRACKS = PLAYLIST_ATTRIBUTES_LABEL.LIB_TRACKS


class PlaylistChildSerializer(BasePlaylistWithoutTracksSerializer):
    uuid = serializers.CharField(source=PLAYLIST_FOREIGN_MODEL_RELATIONS_STR.UUID)
    created_on = serializers.DateTimeField(source=PLAYLIST_FOREIGN_MODEL_RELATIONS_STR.CREATED_ON)
    library_tracks_count = serializers.SerializerMethodField()
    library_tracks = LibTrackWithoutAlbumAndPlaylistSerializer(source=PLAYLIST_FOREIGN_MODEL_RELATIONS_STR.LIB_TRACKS,
                                                               many=True)

    def get_library_tracks_count(self, obj) -> int:
        return obj.playlist.library_tracks.count()

    class Meta:
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.CREATED_ON,
                  FIELDS.LIB_TRACKS_COUNT,
                  FIELDS.LIB_TRACKS]
