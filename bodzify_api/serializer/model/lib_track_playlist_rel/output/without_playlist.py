from rest_framework import serializers

from bodzify_api.model.uploaded_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel
from bodzify_api.serializer.model.uploaded_track.output.detailed import UploadedTrackDetailedSerializer

from .Fields import Fields


class LibTrackPlaylistRelWithoutPlaylist(serializers.ModelSerializer):
    library_track = UploadedTrackDetailedSerializer(source=Fields.LIB_TRACK_INTERNAL)

    class Meta:
        model = LibTrackPlaylistRel
        fields = [Fields.LIB_TRACK_PUBLIC, Fields.POSITION,]
