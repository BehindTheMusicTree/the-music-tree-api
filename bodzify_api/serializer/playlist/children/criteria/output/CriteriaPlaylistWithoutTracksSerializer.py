#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.playlist.children.CriteriaPlaylist import ATTRIBUTES_LABEL, CriteriaPlaylist
from bodzify_api.serializer.playlist.children.PlaylistChildSerializer \
    import PlaylistChildSerializer, FIELDS as PLAYLIST_CHILD_FIELDS
from bodzify_api.serializer.playlist.children.criteria.output.CriteriaPlaylistWithoutTracksAndParentAndRootSerializer \
    import CriteriaPlaylistWithoutTracksAndParentAndRootSerializer


class FIELDS:
    UUID = PLAYLIST_CHILD_FIELDS.UUID
    NAME = PLAYLIST_CHILD_FIELDS.NAME
    ADDED_ON = PLAYLIST_CHILD_FIELDS.ADDED_ON
    PARENT = ATTRIBUTES_LABEL.PARENT
    ROOT = ATTRIBUTES_LABEL.ROOT
    LIB_TRACKS_COUNT = PLAYLIST_CHILD_FIELDS.LIB_TRACKS_COUNT


class CriteriaPlaylistWithoutTracksSerializer(CriteriaPlaylistWithoutTracksAndParentAndRootSerializer):
    parent = CriteriaPlaylistWithoutTracksAndParentAndRootSerializer()
    root = CriteriaPlaylistWithoutTracksAndParentAndRootSerializer()

    def get_name(self, obj):
        return obj.name

    def to_representation(self, instance):
        assert isinstance(instance, CriteriaPlaylist), f"Expected a CriteriaPlaylist, got {type(instance)}"
        return super().to_representation(instance)

    class Meta:
        model = CriteriaPlaylist
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.ADDED_ON,
                  FIELDS.PARENT,
                  FIELDS.ROOT,
                  FIELDS.LIB_TRACKS_COUNT]
