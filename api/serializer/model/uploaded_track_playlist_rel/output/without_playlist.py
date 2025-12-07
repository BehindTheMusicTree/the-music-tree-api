from rest_framework import serializers

from api.model.uploaded_track_playlist_rel.UploadedTrackPlaylistRel import UploadedTrackPlaylistRel
from api.serializer.model.uploaded_track.output.detailed import UploadedTrackDetailedSerializer

from .Fields import Fields


class UploadedTrackPlaylistRelWithoutPlaylist(serializers.ModelSerializer):
    uploaded_track = UploadedTrackDetailedSerializer()

    class Meta:
        model = UploadedTrackPlaylistRel
        fields = [Fields.UPLOADED_TRACK_PUBLIC, Fields.POSITION,]
