#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.track.LibraryTrack import LibraryTrack, ATTRIBUTES_LABEL
from bodzify_api.serializer.artist.with_only_name import ArtistWithOnlyNameSerializer
from bodzify_api.serializer.album.output.without_track import AlbumWithoutTracksSerializer
from bodzify_api.serializer.criteria.output.simple import CriteriaSimpleSerializer
from bodzify_api.serializer.musicbrainz.recording.detailed import MusicbrainzRecordingDetailedSerializer
from bodzify_api.serializer.playlist.base.output.without_tracks import BasePlaylistWithoutTracksSerializer
from bodzify_api.serializer.track_file.output.detailed import FileDetailedSerializer
from bodzify_api.test.view.track.input.method.create.attributes import musicbrainz_recording


class FIELDS:
    UUID = ATTRIBUTES_LABEL.UUID
    RELATIVE_URL = ATTRIBUTES_LABEL.RELATIVE_URL
    FILE = ATTRIBUTES_LABEL.TRACK_FILE_USER_FRIENDLY
    DURATION_IN_SEC = ATTRIBUTES_LABEL.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = ATTRIBUTES_LABEL.DURATION_STR_IN_HOUR_MIN_SEC
    MUSICBRAINZ_RECORDING = ATTRIBUTES_LABEL.MUSICBRAINZ_RECORDING
    TITLE = ATTRIBUTES_LABEL.TITLE
    ARTIST = ATTRIBUTES_LABEL.ARTIST
    ALBUM = ATTRIBUTES_LABEL.ALBUM
    GENRE = ATTRIBUTES_LABEL.GENRE
    RATING = ATTRIBUTES_LABEL.RATING
    LANGUAGE = ATTRIBUTES_LABEL.LANGUAGE
    BASE_PLAYLISTS_USER_FRIENDLY = ATTRIBUTES_LABEL.BASE_PLAYLISTS_USER_FRIENDLY
    CREATED_ON = ATTRIBUTES_LABEL.CREATED_ON
    PLAY_COUNT = ATTRIBUTES_LABEL.PLAY_COUNT


class LibTrackDetailedSerializer(serializers.ModelSerializer):
    musicbrainz_recording = MusicbrainzRecordingDetailedSerializer()
    file = FileDetailedSerializer(source=ATTRIBUTES_LABEL.TRACK_FILE)
    artist = ArtistWithOnlyNameSerializer()
    album = AlbumWithoutTracksSerializer()
    genre = CriteriaSimpleSerializer()
    playlists = BasePlaylistWithoutTracksSerializer(source=ATTRIBUTES_LABEL.BASE_PLAYLISTS, many=True)

    class Meta:
        model = LibraryTrack
        fields = [FIELDS.UUID,
                  FIELDS.RELATIVE_URL,
                  FIELDS.FILE,
                  FIELDS.DURATION_IN_SEC,
                  FIELDS.DURATION_STR_IN_HOUR_MIN_SEC,
                  FIELDS.MUSICBRAINZ_RECORDING,
                  FIELDS.TITLE,
                  FIELDS.ARTIST,
                  FIELDS.ALBUM,
                  FIELDS.GENRE,
                  FIELDS.RATING,
                  FIELDS.LANGUAGE,
                  FIELDS.BASE_PLAYLISTS_USER_FRIENDLY,
                  FIELDS.CREATED_ON,
                  FIELDS.PLAY_COUNT]
