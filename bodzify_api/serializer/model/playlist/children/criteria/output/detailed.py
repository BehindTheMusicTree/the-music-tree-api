from rest_framework import serializers

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.model.criteria.output.minimum import CriteriaMinimumSerializer
from bodzify_api.serializer.model.uploaded_track_playlist_rel.output.without_playlist import (
    LibTrackPlaylistRelWithoutPlaylist
)
from bodzify_api.serializer.model.playlist.children.criteria.output.minumum import CriteriaPlaylistMinimumSerializer

from .Fields import Fields


class CriteriaPlaylistDetailedSerializer(serializers.ModelSerializer):
    library_track_playlist_relations = LibTrackPlaylistRelWithoutPlaylist(
        source=Fields.UPLOADED_TRACK_PLAYLIST_RELS_INTERNAL, many=True)
    library_tracks_count = serializers.IntegerField(source=Fields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL)
    library_tracks_archived_count = serializers.IntegerField(source=Fields.UPLOADED_TRACKS_ARCHIVED_COUNT_INTERNAL)
    criteria = CriteriaMinimumSerializer()
    root = CriteriaPlaylistMinimumSerializer()  # type: ignore
    parent = CriteriaPlaylistMinimumSerializer()

    class Meta:
        model = CriteriaPlaylist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.UPLOADED_TRACK_PLAYLIST_RELS_PUBLIC,
                  Fields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,
                  Fields.UPLOADED_TRACKS_ARCHIVED_COUNT_PUBLIC,
                  Fields.CRITERIA,
                  Fields.PARENT,
                  Fields.ROOT,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON,]
