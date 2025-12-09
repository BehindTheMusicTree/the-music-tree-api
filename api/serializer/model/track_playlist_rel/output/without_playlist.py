from rest_framework import serializers

from api.model.track_playlist_rel.TrackPlaylistRel import TrackPlaylistRel
from api.serializer.model.track.output.detailed import TrackDetailedSerializer

from .Fields import Fields


class TrackPlaylistRelWithoutPlaylist(serializers.ModelSerializer):
    track = TrackDetailedSerializer()

    class Meta:
        model = TrackPlaylistRel
        fields = [Fields.TRACK_PUBLIC, Fields.POSITION,]
