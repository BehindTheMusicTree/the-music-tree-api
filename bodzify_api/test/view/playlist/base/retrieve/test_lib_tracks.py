#!/usr/bin/env python

from rest_framework import status

from bodzify_api.utils.utils import to_camel_case
from bodzify_api.test.view.playlist.base.BasePlaylistTestCase import BasePlaylistTestCase
from bodzify_api.serializer.track.output.simple_without_playlists_and_album import Fields as LibTrackGetFields
from bodzify_api.serializer.playlist.children.criteria.output.detailed import Fields as CriteriaPlaylistFields


class TestCase(BasePlaylistTestCase):

    def test_retrieve_then_lib_track_ordered_by_date_added_desc(self):
        genre_name = 'rock'
        genre = self.model_fixture_factory.create_genre(name=genre_name)

        lib_track3 = self.model_fixture_factory.create_lib_track(title="Love3", genre=genre)
        lib_track2 = self.model_fixture_factory.create_lib_track(title="Love2", genre=genre)
        lib_track1 = self.model_fixture_factory.create_lib_track(title="Love1", genre=genre)

        response = self._retrieve(base_playlist_uuid=genre.criteria_playlist.base_playlist.uuid)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        result_tracks = result[to_camel_case(CriteriaPlaylistFields.LIB_TRACKS)]
        assert result_tracks[0][to_camel_case(LibTrackGetFields.TITLE)] == lib_track1.title
        assert result_tracks[1][to_camel_case(LibTrackGetFields.TITLE)] == lib_track2.title
        assert result_tracks[2][to_camel_case(LibTrackGetFields.TITLE)] == lib_track3.title

    def test_duration(self):
        genre = self.model_fixture_factory.create_genre(name='rock')

        track_intodeep = self.model_fixture_factory.create_lib_track(title="In Too Deep", genre=genre)
        track_summer = self.model_fixture_factory.create_lib_track(title="Summer", genre=genre)
        tracks_duration_in_sec = track_intodeep.duration_in_sec + track_summer.duration_in_sec  # type: ignore
        response = self._retrieve(genre.criteria_playlist.uuid)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result[to_camel_case(CriteriaPlaylistFields.DURATION_IN_SEC)] == tracks_duration_in_sec

    def test_count(self):
        genre = self.model_fixture_factory.create_genre(name='rock')
        self.model_fixture_factory.create_lib_track(title="In Too Deep", genre=genre)
        self.model_fixture_factory.create_lib_track(title="Summer", genre=genre)
        self.model_fixture_factory.create_lib_track(title="Winter", genre=genre, archived=True)
        response = self._retrieve(genre.criteria_playlist.uuid)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result[to_camel_case(CriteriaPlaylistFields.LIB_TRACKS_COUNT)] == 2

    def test_archived_count(self):
        genre = self.model_fixture_factory.create_genre(name='rock')
        self.model_fixture_factory.create_lib_track(title="In Too Deep", genre=genre)
        self.model_fixture_factory.create_lib_track(title="Summer", genre=genre, archived=True)
        self.model_fixture_factory.create_lib_track(title="Summer2", genre=genre, archived=True)
        self.model_fixture_factory.create_lib_track(title="Summer3", genre=genre, archived=True)
        response = self._retrieve(genre.criteria_playlist.uuid)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result[to_camel_case(CriteriaPlaylistFields.LIB_TRACKS_ARCHIVED_COUNT)] == 3
