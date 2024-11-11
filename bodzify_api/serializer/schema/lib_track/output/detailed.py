from rest_framework import serializers

from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack, Fields as ModelFields
from bodzify_api.serializer.schema.lib_track.output.Fields import Fields
from bodzify_api.serializer.schema.album.minimum import AlbumMinimumSerializer
from bodzify_api.serializer.schema.artist.minimum import ArtistMinimumSerializer
from bodzify_api.serializer.schema.criteria.output.minimum import CriteriaMinimumSerializer
from bodzify_api.serializer.schema.playlist.base.output.minimum import BasePlaylistMinimumSerializer
from bodzify_api.serializer.schema.track_file.output.detailed import FileDetailedSerializer


class LibTrackDetailedSerializer(serializers.ModelSerializer):
    file = FileDetailedSerializer(source=ModelFields.TRACK_FILE)
    artists = ArtistMinimumSerializer(many=True)
    album = AlbumMinimumSerializer()
    genre = CriteriaMinimumSerializer()
    playlists = BasePlaylistMinimumSerializer(source=ModelFields.BASE_PLAYLISTS, many=True)

    class Meta:
        model = LibraryTrack
        fields = [Fields.UUID,
                  Fields.RELATIVE_URL,
                  Fields.TITLE,
                  Fields.FILE,
                  Fields.ARTISTS,
                  Fields.ALBUM,
                  Fields.POSITION_IN_ALBUM,
                  Fields.GENRE,
                  Fields.RATING,
                  Fields.LANGUAGE,
                  Fields.BASE_PLAYLISTS_USER_FRIENDLY,
                  Fields.PLAY_COUNT,
                  Fields.ARCHIVED,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON,]
