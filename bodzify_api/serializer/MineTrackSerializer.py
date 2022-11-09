from rest_framework import serializers

from bodzify_api.models import MineTrack

class MineTrackSerializer(serializers.Serializer):
    class Meta:
        model = MineTrack
        fields = [
            "title", 
            "artist", 
            "duration",
            "releasedOn",
            "url"]