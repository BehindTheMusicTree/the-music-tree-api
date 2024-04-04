#!/usr/bin/env python

import logging
from rest_framework import status
from ddf import G

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.playlist.mother.output.PlaylistWithTracksSerializer import FIELDS as RETRIEVE_FIELDS
from bodzify_api.test.view.playlist.mother.PlaylistTestCase import PlaylistTestCase
from bodzify_api.utils import to_camel_case
from bodzify_api.serializer.track.output.LibTrackWithoutAlbumAndPlaylistSerializer import FIELDS as LIB_TRACK_FIELDS
from bodzify_api.serializer.playlist_library_track.output.PlaylistLibTrackRelationWithoutPlaylist \
    import FIELDS as PLAYLIST_LIB_TRACK_RELATION_FIELDS

logger = logging.getLogger('bodyzify_api')


class TestCase(PlaylistTestCase):

    def test_retrieve_simple_then_ok(self):
        name = 'cuisine'
        playlist_uuid = G(SimplePlaylist, playlist__user=self.test_user, name=name).playlist.uuid  # type: ignore

        response = self.retrieve_playlist(uuid=playlist_uuid)
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.result[RETRIEVE_FIELDS.NAME] == name

    def test_retrieve_genre_then_ok(self):
        name = 'rock'
        genre = G(Criteria, user=self.test_user, name=name, type=CRITERIA_TYPES_ID.GENRE)
        playlist_uuid = Playlist.objects.get(user=self.test_user,
                                             criteria_playlist__criteria=genre,
                                             criteria_playlist__type=CRITERIA_TYPES_ID.GENRE).uuid  # type: ignore

        response = self.retrieve_playlist(uuid=playlist_uuid)
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.result[RETRIEVE_FIELDS.NAME] == name

    def test_retrieve_tag_then_ok(self):
        name = 'fr'
        genre = G(Criteria, user=self.test_user, name=name, type=CRITERIA_TYPES_ID.TAG)
        playlist_uuid = Playlist.objects.get(user=self.test_user,
                                             criteria_playlist__criteria=genre,
                                             criteria_playlist__type=CRITERIA_TYPES_ID.TAG).uuid  # type: ignore

        response = self.retrieve_playlist(uuid=playlist_uuid)
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.result[RETRIEVE_FIELDS.NAME] == name

    def test_retrieve_then_lib_track_ordered_by_position(self):
        genre_name = 'rock'
        genre = G(Criteria, user=self.test_user, name=genre_name, type=CRITERIA_TYPES_ID.TAG)

        lib_track3 = G(LibraryTrack, user=self.test_user, title="Love", genre=genre)
        lib_track2 = G(LibraryTrack, user=self.test_user, title="Loves", genre=genre)
        lib_track1 = G(LibraryTrack, user=self.test_user, title="Lovdddde", genre=genre)

        response = self.retrieve_playlist(uuid=genre.criteria_playlist.playlist.uuid)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        result_tracks = self.result[to_camel_case(RETRIEVE_FIELDS.LIB_TRACKS)]
        assert result_tracks[0][
            to_camel_case(PLAYLIST_LIB_TRACK_RELATION_FIELDS.LIB_TRACK)][
            LIB_TRACK_FIELDS.TITLE] == lib_track1.title  # type: ignore
        assert result_tracks[1][
            to_camel_case(PLAYLIST_LIB_TRACK_RELATION_FIELDS.LIB_TRACK)][
            LIB_TRACK_FIELDS.TITLE] == lib_track2.title  # type: ignore
        assert result_tracks[2][
            to_camel_case(PLAYLIST_LIB_TRACK_RELATION_FIELDS.LIB_TRACK)][
            LIB_TRACK_FIELDS.TITLE] == lib_track3.title  # type: ignore
