#!/usr/bin/env python

from unittest import result
from rest_framework import status

from bodzify_api.utils.utils import to_camel_case
from bodzify_api.test.view.album.AlbumViewTestCase import AlbumViewTestCase
from bodzify_api.serializer.album.detailed import Fields as RetrieveFields
from bodzify_api.serializer.track.output.simple_without_playlists_and_album import Fields as LibTrackGetFields


class TestCase(AlbumViewTestCase):

    def test_all_lib_tracks_with_positions_then_order_by_position_asc(self):
        album = self.model_fixture_factory.create_album(name="Chuck")
        lib_track_12th_position = self.model_fixture_factory.create_lib_track(
            title="Love", album=album, position_in_album=12)
        lib_track_45th_position = self.model_fixture_factory.create_lib_track(
            title="Loves", album=album, position_in_album=45)
        lib_track_1st_position = self.model_fixture_factory.create_lib_track(
            title="Lovdddde", album=album, position_in_album=1)

        response = self._retrieve(album_uuid=album.uuid)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        result_tracks = result[to_camel_case(RetrieveFields.LIB_TRACKS)]

        assert result_tracks[0][to_camel_case(LibTrackGetFields.TITLE)] == lib_track_1st_position.title
        assert result_tracks[1][to_camel_case(LibTrackGetFields.TITLE)] == lib_track_12th_position.title
        assert result_tracks[2][to_camel_case(LibTrackGetFields.TITLE)] == lib_track_45th_position.title

    def test_some_lib_tracks_with_positions_then_order_by_position_asc_then_those_with_no_position_by_title_asc(self):
        album = self.model_fixture_factory.create_album(name="Chuck")
        lib_track_112th_position = self.model_fixture_factory.create_lib_track(
            title="Love", album=album, position_in_album=112)
        lib_track_4th_position = self.model_fixture_factory.create_lib_track(
            title="Loves", album=album, position_in_album=2)
        lib_track_no_position_3 = self.model_fixture_factory.create_lib_track(title="Lovdddde", album=album)
        lib_track_no_position_4 = self.model_fixture_factory.create_lib_track(title="Movee", album=album)
        lib_track_no_position_2 = self.model_fixture_factory.create_lib_track(title="Jooove", album=album)
        lib_track_no_position_1 = self.model_fixture_factory.create_lib_track(title="Ave", album=album)

        response = self._retrieve(album_uuid=album.uuid)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        result_tracks = result[to_camel_case(RetrieveFields.LIB_TRACKS)]

        assert result_tracks[0][to_camel_case(LibTrackGetFields.TITLE)] == lib_track_4th_position.title
        assert result_tracks[1][to_camel_case(LibTrackGetFields.TITLE)] == lib_track_112th_position.title
        assert result_tracks[2][to_camel_case(LibTrackGetFields.TITLE)] == lib_track_no_position_1.title
        assert result_tracks[3][to_camel_case(LibTrackGetFields.TITLE)] == lib_track_no_position_2.title
        assert result_tracks[4][to_camel_case(LibTrackGetFields.TITLE)] == lib_track_no_position_3.title
        assert result_tracks[5][to_camel_case(LibTrackGetFields.TITLE)] == lib_track_no_position_4.title

    def test_duration(self):
        album = self.model_fixture_factory.create_album(name="Chuck")
        track_intodeep = self.model_fixture_factory.create_lib_track(title="In Too Deep", album=album)
        track_summer = self.model_fixture_factory.create_lib_track(title="Summer", album=album)
        tracks_duration_in_sec = track_intodeep.duration_in_sec + track_summer.duration_in_sec  # type: ignore
        response = self._retrieve(album.uuid)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result[to_camel_case(RetrieveFields.DURATION_IN_SEC)] == tracks_duration_in_sec

    def test_count(self):
        album = self.model_fixture_factory.create_album(name="Chuck")
        self.model_fixture_factory.create_lib_track(title="In Too Deep", album=album)
        self.model_fixture_factory.create_lib_track(title="Summer", album=album)
        response = self._retrieve(album.uuid)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result[to_camel_case(RetrieveFields.LIB_TRACKS_COUNT)] == 2

    def test_archived_count(self):
        album = self.model_fixture_factory.create_album(name="Chuck")
        self.model_fixture_factory.create_lib_track(title="In Too Deep", album=album)
        self.model_fixture_factory.create_lib_track(title="Summer", album=album, archived=True)
        self.model_fixture_factory.create_lib_track(title="Summer2", album=album, archived=True)
        self.model_fixture_factory.create_lib_track(title="Summer3", album=album, archived=True)
        response = self._retrieve(album.uuid)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result[to_camel_case(RetrieveFields.LIB_TRACKS_ARCHIVED_COUNT)] == 3
