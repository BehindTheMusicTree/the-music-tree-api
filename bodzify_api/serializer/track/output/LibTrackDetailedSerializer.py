#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.track.LibraryTrack import LibraryTrack, ATTRIBUTES_LABEL
from bodzify_api.serializer.artist.ArtistWithOnlyNameSerializer import ArtistWithOnlyNameSerializer
from bodzify_api.serializer.album.output.AlbumWithoutTracksSerializer import AlbumWithoutTracksSerializer
from bodzify_api.serializer.criteria.output.CriteriaSimpleSerializer import CriteriaSimpleSerializer
from bodzify_api.serializer.musicbrainz.recording.MusicbrainzRecordingSerializer import MusicbrainzRecordingDetailedSerializer
from bodzify_api.serializer.playlist.base.output.without_track import BasePlaylistWithoutTrackSerializer
from bodzify_api.serializer.track_file.output.FileDetailedSerializer import FileDetailedSerializer
from bodzify_api.test.view.track.input.method.create.attributes import musicbrainz_recording


class FIELDS:
    UUID = ATTRIBUTES_LABEL.UUID
    RELATIVE_URL = ATTRIBUTES_LABEL.RELATIVE_URL
    FILE = ATTRIBUTES_LABEL.TRACK_FILE_USER_FRIENDLY
    DURATION = ATTRIBUTES_LABEL.DURATION
    MUSICBRAINZ_RECORDING = ATTRIBUTES_LABEL.MUSICBRAINZ_RECORDING
    TITLE = ATTRIBUTES_LABEL.TITLE
    ARTIST = ATTRIBUTES_LABEL.ARTIST
    ALBUM = ATTRIBUTES_LABEL.ALBUM
    GENRE = ATTRIBUTES_LABEL.GENRE
    RATING = ATTRIBUTES_LABEL.RATING
    LANGUAGE = ATTRIBUTES_LABEL.LANGUAGE
    PLAYLISTS = ATTRIBUTES_LABEL.PLAYLISTS
    CREATED_ON = ATTRIBUTES_LABEL.CREATED_ON
    PLAY_COUNT = ATTRIBUTES_LABEL.PLAY_COUNT


class LibTrackDetailedSerializer(serializers.ModelSerializer):
    musicbrainz_recording = MusicbrainzRecordingDetailedSerializer()
    file = FileDetailedSerializer(source=ATTRIBUTES_LABEL.TRACK_FILE)
    artist = ArtistWithOnlyNameSerializer()
    album = AlbumWithoutTracksSerializer()
    genre = CriteriaSimpleSerializer()
    playlists = BasePlaylistWithoutTrackSerializer(many=True)

    class Meta:
        model = LibraryTrack
        fields = [FIELDS.UUID,
                  FIELDS.RELATIVE_URL,
                  FIELDS.FILE,
                  FIELDS.DURATION,
                  FIELDS.MUSICBRAINZ_RECORDING,
                  FIELDS.TITLE,
                  FIELDS.ARTIST,
                  FIELDS.ALBUM,
                  FIELDS.GENRE,
                  FIELDS.RATING,
                  FIELDS.LANGUAGE,
                  FIELDS.PLAYLISTS,
                  FIELDS.CREATED_ON,
                  FIELDS.PLAY_COUNT]
