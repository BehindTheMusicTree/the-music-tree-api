#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.track.LibraryTrack import LibraryTrack, AttributesLabels
from bodzify_api.serializer.artist.with_only_name import ArtistWithOnlyNameSerializer
from bodzify_api.serializer.album.without_tracks import AlbumWithoutTracksSerializer
from bodzify_api.serializer.criteria.output.simple import CriteriaSimpleSerializer
from bodzify_api.serializer.musicbrainz.recording.detailed import MusicbrainzRecordingDetailedSerializer
from bodzify_api.serializer.playlist.base.output.without_tracks import BasePlaylistWithoutTracksSerializer
from bodzify_api.serializer.track_file.output.detailed import FileDetailedSerializer


class Fields:
    UUID = AttributesLabels.UUID
    RELATIVE_URL = AttributesLabels.RELATIVE_URL
    FILE = AttributesLabels.TRACK_FILE_USER_FRIENDLY
    DURATION_IN_SEC = AttributesLabels.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = AttributesLabels.DURATION_STR_IN_HOUR_MIN_SEC
    MUSICBRAINZ_RECORDING_LOOKUP_ERROR_CODE = AttributesLabels.MUSICBRAINZ_RECORDING_LOOKUP_ERROR_STR
    MUSICBRAINZ_RECORDING = AttributesLabels.MUSICBRAINZ_RECORDING
    TITLE = AttributesLabels.TITLE
    ARTIST = AttributesLabels.ARTIST
    ALBUM = AttributesLabels.ALBUM
    GENRE = AttributesLabels.GENRE
    RATING = AttributesLabels.RATING
    LANGUAGE = AttributesLabels.LANGUAGE
    BASE_PLAYLISTS_USER_FRIENDLY = AttributesLabels.BASE_PLAYLISTS_USER_FRIENDLY
    PLAY_COUNT = AttributesLabels.PLAY_COUNT
    ARCHIVED = AttributesLabels.ARCHIVED
    CREATED_ON = AttributesLabels.CREATED_ON


class LibTrackDetailedSerializer(serializers.ModelSerializer):
    musicbrainz_recording = MusicbrainzRecordingDetailedSerializer()
    file = FileDetailedSerializer(source=AttributesLabels.TRACK_FILE)
    artist = ArtistWithOnlyNameSerializer()
    album = AlbumWithoutTracksSerializer()
    genre = CriteriaSimpleSerializer()
    playlists = BasePlaylistWithoutTracksSerializer(source=AttributesLabels.BASE_PLAYLISTS, many=True)

    class Meta:
        model = LibraryTrack
        fields = [Fields.UUID,
                  Fields.RELATIVE_URL,
                  Fields.FILE,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,
                  Fields.MUSICBRAINZ_RECORDING,
                  Fields.MUSICBRAINZ_RECORDING_LOOKUP_ERROR_CODE,
                  Fields.TITLE,
                  Fields.ARTIST,
                  Fields.ALBUM,
                  Fields.GENRE,
                  Fields.RATING,
                  Fields.LANGUAGE,
                  Fields.BASE_PLAYLISTS_USER_FRIENDLY,
                  Fields.PLAY_COUNT,
                  Fields.ARCHIVED,
                  Fields.CREATED_ON,]
