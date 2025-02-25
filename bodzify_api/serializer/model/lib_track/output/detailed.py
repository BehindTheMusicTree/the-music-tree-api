from rest_framework import serializers

from bodzify_api.model.track.lib.LibraryTrack import Fields as ModelFields
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.serializer.model.album.minimum import AlbumMinimumSerializer
from bodzify_api.serializer.model.artist.minimum import ArtistMinimumSerializer
from bodzify_api.serializer.model.criteria.output.minimum import \
    CriteriaMinimumSerializer
from bodzify_api.serializer.model.lib_track.output.Fields import Fields
from bodzify_api.serializer.model.playlist.base.output.minimum import \
    PlaylistMinimumSerializer
from bodzify_api.serializer.model.track_file.output.detailed import \
    FileDetailedSerializer


class LibTrackDetailedSerializer(serializers.ModelSerializer):
    file = FileDetailedSerializer(source=ModelFields.TRACK_FILE)
    artists = ArtistMinimumSerializer(many=True)
    album = AlbumMinimumSerializer()
    genre = CriteriaMinimumSerializer()
    playlists = PlaylistMinimumSerializer(many=True)

    class Meta:
        model = LibraryTrack
        fields = [Fields.UUID,
                  Fields.RELATIVE_URL,
                  Fields.TITLE,
                  Fields.FILE,
                  Fields.ARTISTS,
                  Fields.ALBUM,
                  Fields.TRACK_NUMBER,
                  Fields.GENRE,
                  Fields.RATING,
                  Fields.LANGUAGE,
                  Fields.PLAYLISTS_PUBLIC,
                  Fields.PLAY_COUNT,
                  Fields.ARCHIVED,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON,]
