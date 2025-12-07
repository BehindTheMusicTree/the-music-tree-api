from rest_framework import serializers

from api.model.uploaded_track.UploadedTrack import Fields as ModelFields
from api.model.uploaded_track.UploadedTrack import UploadedTrack
from api.serializer.model.album.minimum import AlbumMinimumSerializer
from api.serializer.model.artist.minimum import ArtistMinimumSerializer
from api.serializer.model.criteria.output.minimum import CriteriaMinimumSerializer
from api.serializer.model.uploaded_track.output.Fields import Fields
from api.serializer.model.playlist.base.output.minimum import PlaylistMinimumSerializer
from api.serializer.model.uploaded_track_file.output.detailed import FileDetailedSerializer


class UploadedTrackDetailedSerializer(serializers.ModelSerializer):
    file = FileDetailedSerializer(source=ModelFields.TRACK_FILE_INTERNAL)
    artists = ArtistMinimumSerializer(many=True)
    album = AlbumMinimumSerializer()
    genre = CriteriaMinimumSerializer()
    playlists = PlaylistMinimumSerializer(many=True)

    class Meta:
        model = UploadedTrack
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
