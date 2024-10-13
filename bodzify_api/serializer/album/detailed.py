#!/usr/bin/env python

from bodzify_api.model.Album import Album, AttributesLabels
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.artist.with_only_name import ArtistWithOnlyNameSerializer
from bodzify_api.serializer.lib_track_mixin.detailed import LibTrackMixinSerializer
from bodzify_api.serializer.track.output.for_album_detailed import LibTrackForAlbumDetailedSerializer
from bodzify_api.serializer.track.output.simple_without_playlists_and_album \
    import LibTrackSimpleWithoutPlaylistAndAlbumSerializer


class Fields:
    UUID = AttributesLabels.UUID
    NAME = AttributesLabels.NAME
    YEAR = AttributesLabels.YEAR
    ALBUM_ARTISTS = AttributesLabels.ALBUM_ARTISTS
    LIB_TRACKS = AttributesLabels.LIB_TRACKS
    LIB_TRACKS_COUNT = AttributesLabels.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = AttributesLabels.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = AttributesLabels.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = AttributesLabels.DURATION_STR_IN_HOUR_MIN_SEC


class AlbumDetailedSerializer(LibTrackMixinSerializer):
    album_artists = ArtistWithOnlyNameSerializer(many=True)

    class Meta:
        model = Album
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.YEAR,
                  Fields.ALBUM_ARTISTS,
                  Fields.LIB_TRACKS,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.LIB_TRACKS_ARCHIVED_COUNT,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        sorted_tracks = LibraryTrack.get_sorted_tracks(instance.library_tracks.all())
        representation[AttributesLabels.LIB_TRACKS] = LibTrackForAlbumDetailedSerializer(sorted_tracks, many=True).data
        return representation
