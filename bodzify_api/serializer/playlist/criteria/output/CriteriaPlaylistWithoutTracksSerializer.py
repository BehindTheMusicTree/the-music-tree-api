#!/usr/bin/env python

from bodzify_api.model.playlist.CriteriaPlaylist import ATTRIBUTES_LABEL as CRITERIA_PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.serializer.playlist.output.PlaylistChildWithoutTrackSerializer import PlaylistChildWithoutTrackSerializer


class CriteriaPlaylistWithoutTracksSerializer(PlaylistChildWithoutTrackSerializer):

    class Meta:
        model = CriteriaPlaylist
        fields = [PLAYLIST_ATTRIBUTES_LABEL.UUID,
                  CRITERIA_PLAYLIST_ATTRIBUTES_LABEL.NAME,
                  PLAYLIST_ATTRIBUTES_LABEL.ADDED_ON,
                  CRITERIA_PLAYLIST_ATTRIBUTES_LABEL.PARENT,
                  PLAYLIST_ATTRIBUTES_LABEL.LIBRARY_TRACKS_COUNT]
