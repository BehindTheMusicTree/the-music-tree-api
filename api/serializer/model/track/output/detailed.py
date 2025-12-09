from rest_framework import serializers

from api.model.track.Track import Fields as ModelFields
from api.model.track.Track import Track
from api.serializer.model.album.minimum import AlbumMinimumSerializer
from api.serializer.model.artist.minimum import ArtistMinimumSerializer
from api.serializer.model.criteria.output.minimum import CriteriaMinimumSerializer
from api.serializer.model.track.output.Fields import Fields
from api.serializer.model.playlist.base.output.minimum import PlaylistMinimumSerializer


class TrackDetailedSerializer(serializers.ModelSerializer):
    artists = ArtistMinimumSerializer(many=True)
    album = AlbumMinimumSerializer()
    genre = CriteriaMinimumSerializer()
    playlists = PlaylistMinimumSerializer(many=True)

    class Meta:
        model = Track
        fields = [Fields.UUID,
                  Fields.RELATIVE_URL,
                  Fields.TITLE,
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
