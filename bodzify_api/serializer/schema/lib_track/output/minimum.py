from rest_framework import serializers

from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack, Fields as ModelFields
from bodzify_api.serializer.schema.lib_track.output.Fields import Fields
from bodzify_api.serializer.schema.album.minimum import AlbumMinimumSerializer
from bodzify_api.serializer.schema.artist.minimum import ArtistMinimumSerializer
from bodzify_api.serializer.schema.criteria.output.minimum import CriteriaMinimumSerializer
from bodzify_api.serializer.schema.playlist.base.output.minimum import PlaylistMinimumSerializer
from bodzify_api.serializer.schema.track_file.output.detailed import FileDetailedSerializer


class LibTrackMinimumSerializer(serializers.ModelSerializer):
    artists = ArtistMinimumSerializer(many=True)

    class Meta:
        model = LibraryTrack
        fields = [Fields.UUID,
                  Fields.TITLE,
                  Fields.ARTISTS]
