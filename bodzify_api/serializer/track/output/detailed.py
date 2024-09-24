#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.track.LibraryTrack import LibraryTrack, AttributesLabel
from bodzify_api.serializer.artist.with_only_name import ArtistWithOnlyNameSerializer
from bodzify_api.serializer.album.without_track import AlbumWithoutTracksSerializer
from bodzify_api.serializer.criteria.output.simple import CriteriaSimpleSerializer
from bodzify_api.serializer.musicbrainz.recording.detailed import MusicbrainzRecordingDetailedSerializer
from bodzify_api.serializer.playlist.base.output.without_tracks import BasePlaylistWithoutTracksSerializer
from bodzify_api.serializer.track_file.output.detailed import FileDetailedSerializer


class FIELDS:
    UUID = AttributesLabel.UUID
    RELATIVE_URL = AttributesLabel.RELATIVE_URL
    FILE = AttributesLabel.TRACK_FILE_USER_FRIENDLY
    DURATION_IN_SEC = AttributesLabel.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = AttributesLabel.DURATION_STR_IN_HOUR_MIN_SEC
    MUSICBRAINZ_RECORDING_LOOKUP_ERROR_CODE = AttributesLabel.MUSICBRAINZ_RECORDING_LOOKUP_ERROR_STR
    MUSICBRAINZ_RECORDING = AttributesLabel.MUSICBRAINZ_RECORDING
    TITLE = AttributesLabel.TITLE
    ARTIST = AttributesLabel.ARTIST
    ALBUM = AttributesLabel.ALBUM
    GENRE = AttributesLabel.GENRE
    RATING = AttributesLabel.RATING
    LANGUAGE = AttributesLabel.LANGUAGE
    BASE_PLAYLISTS_USER_FRIENDLY = AttributesLabel.BASE_PLAYLISTS_USER_FRIENDLY
    CREATED_ON = AttributesLabel.CREATED_ON
    PLAY_COUNT = AttributesLabel.PLAY_COUNT


class LibTrackDetailedSerializer(serializers.ModelSerializer):
    musicbrainz_recording = MusicbrainzRecordingDetailedSerializer()
    file = FileDetailedSerializer(source=AttributesLabel.TRACK_FILE)
    artist = ArtistWithOnlyNameSerializer()
    album = AlbumWithoutTracksSerializer()
    genre = CriteriaSimpleSerializer()
    playlists = BasePlaylistWithoutTracksSerializer(source=AttributesLabel.BASE_PLAYLISTS, many=True)

    class Meta:
        model = LibraryTrack
        fields = [FIELDS.UUID,
                  FIELDS.RELATIVE_URL,
                  FIELDS.FILE,
                  FIELDS.DURATION_IN_SEC,
                  FIELDS.DURATION_STR_IN_HOUR_MIN_SEC,
                  FIELDS.MUSICBRAINZ_RECORDING,
                  FIELDS.MUSICBRAINZ_RECORDING_LOOKUP_ERROR_CODE,
                  FIELDS.TITLE,
                  FIELDS.ARTIST,
                  FIELDS.ALBUM,
                  FIELDS.GENRE,
                  FIELDS.RATING,
                  FIELDS.LANGUAGE,
                  FIELDS.BASE_PLAYLISTS_USER_FRIENDLY,
                  FIELDS.CREATED_ON,
                  FIELDS.PLAY_COUNT]
