from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.serializer.AppModelSerializer import AppModelSerializer
from bodzify_api.serializer.schema.model.artist.minimum import ArtistMinimumSerializer
from bodzify_api.serializer.schema.model.lib_track.output.simple.Fields import Fields as SimpleFields


class Fields:
    UUID = SimpleFields.UUID
    TITLE = SimpleFields.TITLE
    ARTISTS = SimpleFields.ARTISTS
    RATING = SimpleFields.RATING
    LANGUAGE = SimpleFields.LANGUAGE
    PLAY_COUNT = SimpleFields.PLAY_COUNT


class LibTrackWithoutAlbumPlaylistGenreSerializer(AppModelSerializer):
    artists = ArtistMinimumSerializer(many=True)

    class Meta:
        model = LibraryTrack
        fields = [
            Fields.UUID,
            Fields.TITLE,
            Fields.ARTISTS,
            Fields.RATING,
            Fields.LANGUAGE,
            Fields.PLAY_COUNT
        ]
