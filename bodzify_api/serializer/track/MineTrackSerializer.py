from rest_framework import serializers

from bodzify_api.model.track.MineTrack import MineTrack


class MineTrackSerializer(serializers.Serializer):


    class Meta:
        model = MineTrack
        fields = [
            "title", 
            "artist", 
            "duration",
            "releasedOn",
            "url"]