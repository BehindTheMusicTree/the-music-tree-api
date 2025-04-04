from rest_framework import serializers

from bodzify_api.model.uploaded_track_playlist_rel.UploadedTrackPlaylistRel import UploadedTrackPlaylistRel
from bodzify_api.serializer.model.playlist.base.output.minimum import PlaylistMinimumSerializer

from .Fields import Fields


class LibTrackPlaylistRelWithoutLibTrack(serializers.ModelSerializer):
    playlist = PlaylistMinimumSerializer()

    class Meta:
        model = UploadedTrackPlaylistRel
        fields = [Fields.PLAYLIST,
                  Fields.POSITION]
