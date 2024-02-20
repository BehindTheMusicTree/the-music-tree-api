#!/usr/bin/env python

from yaml import serialize
from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist, \
    ATTRIBUTES_LABEL as CRITERIA_PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.serializer.track.output.TrackWithoutAlbumAndPlaylistSerializer import TrackWithoutAlbumAndPlaylistSerializer
from bodzify_api.serializer.track.output.TrackWithoutPlaylistsAndGenreSerializer import TrackWithoutPlaylistsAndGenreSerializer
from rest_framework import serializers
from bodzify_api.model.playlist.Playlist import FOREIGN_MODEL_ATTRIBUTES_LABEL as \
PLAYLIST_FOREIGN_MODEL_ATTRIBUTES_LABEL, FOREIGN_MODEL_RELATIONS_STR as PLAYLIST_FOREIGN_MODEL_RELATIONS_STR
from bodzify_api.serializer.playlist.criteria.output.CriteriaPlaylistWithoutTracksSerializer import \
    CriteriaPlaylistWithoutTracksSerializer


class CriteriaPlaylistWithTracksSerializer(CriteriaPlaylistWithoutTracksSerializer):

    playlist_uuid = serializers.CharField(source=PLAYLIST_FOREIGN_MODEL_RELATIONS_STR.UUID)
    playlist_added_on = serializers.DateTimeField(source=PLAYLIST_FOREIGN_MODEL_RELATIONS_STR.ADDED_ON)
    playlist_track_count = serializers.IntegerField(source=PLAYLIST_FOREIGN_MODEL_RELATIONS_STR.TRACK_COUNT)
    playlist_librarytracks = TrackWithoutAlbumAndPlaylistSerializer(
        source=PLAYLIST_FOREIGN_MODEL_RELATIONS_STR.LIBRARY_TRACKS, many=True, read_only=True)

    class Meta:
        model = CriteriaPlaylist
        fields = [PLAYLIST_FOREIGN_MODEL_ATTRIBUTES_LABEL.UUID,
                  CRITERIA_PLAYLIST_ATTRIBUTES_LABEL.NAME,
                  PLAYLIST_FOREIGN_MODEL_ATTRIBUTES_LABEL.ADDED_ON,
                  CRITERIA_PLAYLIST_ATTRIBUTES_LABEL.PARENT,
                  PLAYLIST_FOREIGN_MODEL_ATTRIBUTES_LABEL.TRACK_COUNT,
                  PLAYLIST_FOREIGN_MODEL_ATTRIBUTES_LABEL.LIBRARY_TRACKS]
