from rest_framework import status

from bodzify_api.utils.data_transformer import to_camel_case
from bodzify_api.test.view.album.AlbumTestCase import AlbumTestCase
from bodzify_api.serializer.schema.album.detailed import Fields as RetrieveFields
from bodzify_api.serializer.schema.lib_track.output.simple.simple_without_album import Fields as LibTrackGetFields


class TestCase(AlbumTestCase):

    def test_all_lib_tracks_with_positions_then_order_by_position_asc(self):
        album = self.model_fixture_factory.create_album(name="Chuck")
        lib_track_12th_position = self.model_fixture_factory.create_lib_track_with_file(
            title="Love", album=album, position_in_album=12)
        lib_track_45th_position = self.model_fixture_factory.create_lib_track_with_file(
            title="Loves", album=album, position_in_album=45)
        lib_track_1st_position = self.model_fixture_factory.create_lib_track_with_file(
            title="Lovdddde", album=album, position_in_album=1)

        response = self._retrieve_album(album_uuid=album.uuid)

        assert response.status_code == status.HTTP_200_OK
        result_tracks = self.result[to_camel_case(RetrieveFields.LIB_TRACKS)]

        assert result_tracks[0][to_camel_case(LibTrackGetFields.TITLE)] == lib_track_1st_position.title
        assert result_tracks[1][to_camel_case(LibTrackGetFields.TITLE)] == lib_track_12th_position.title
        assert result_tracks[2][to_camel_case(LibTrackGetFields.TITLE)] == lib_track_45th_position.title

    def test_some_lib_tracks_with_positions_then_order_by_position_asc_then_those_with_no_position_by_title_asc(self):
        album = self.model_fixture_factory.create_album(name="Chuck")
        lib_track_112th_position = self.model_fixture_factory.create_lib_track_with_file(
            title="Love", album=album, position_in_album=112)
        lib_track_4th_position = self.model_fixture_factory.create_lib_track_with_file(
            title="Loves", album=album, position_in_album=2)
        lib_track_no_position_3 = self.model_fixture_factory.create_lib_track_with_file(title="Lovdddde", album=album)
        lib_track_no_position_4 = self.model_fixture_factory.create_lib_track_with_file(title="Movee", album=album)
        lib_track_no_position_2 = self.model_fixture_factory.create_lib_track_with_file(title="Jooove", album=album)
        lib_track_no_position_1 = self.model_fixture_factory.create_lib_track_with_file(title="Ave", album=album)

        response = self._retrieve_album(album_uuid=album.uuid)
        assert response.status_code == status.HTTP_200_OK
        result_tracks = self.result[to_camel_case(RetrieveFields.LIB_TRACKS)]

        assert result_tracks[0][to_camel_case(LibTrackGetFields.TITLE)] == lib_track_4th_position.title
        assert result_tracks[1][to_camel_case(LibTrackGetFields.TITLE)] == lib_track_112th_position.title
        assert result_tracks[2][to_camel_case(LibTrackGetFields.TITLE)] == lib_track_no_position_1.title
        assert result_tracks[3][to_camel_case(LibTrackGetFields.TITLE)] == lib_track_no_position_2.title
        assert result_tracks[4][to_camel_case(LibTrackGetFields.TITLE)] == lib_track_no_position_3.title
        assert result_tracks[5][to_camel_case(LibTrackGetFields.TITLE)] == lib_track_no_position_4.title

    def test_duration(self):
        album = self.model_fixture_factory.create_album(name="Chuck")
        self.model_fixture_factory.create_lib_track_with_file(title='ciline',
                                                              album=album,
                                                              filename="Celinekin Park 284 sec.mp3")
        self.model_fixture_factory.create_lib_track_with_file(title='tokyo',
                                                              album=album,
                                                              filename="tokyo drift x sean paul 152 sec.mp3")

        response = self._retrieve_album(album.uuid)
        assert response.status_code == status.HTTP_200_OK
        assert self.result[to_camel_case(RetrieveFields.DURATION_IN_SEC)] == 284 + 152

    def test_count(self):
        album = self.model_fixture_factory.create_album(name="Chuck")
        self.model_fixture_factory.create_lib_track_with_file(title="In Too Deep", album=album)
        self.model_fixture_factory.create_lib_track_with_file(title="Summer", album=album)
        response = self._retrieve_album(album.uuid)
        assert response.status_code == status.HTTP_200_OK
        assert self.result[to_camel_case(RetrieveFields.LIB_TRACKS_COUNT)] == 2

    def test_archived_count(self):
        album = self.model_fixture_factory.create_album(name="Chuck")
        self.model_fixture_factory.create_lib_track_with_file(title="In Too Deep", album=album)
        self.model_fixture_factory.create_lib_track_with_file(title="Summer", album=album, archived=True)
        self.model_fixture_factory.create_lib_track_with_file(title="Summer2", album=album, archived=True)
        self.model_fixture_factory.create_lib_track_with_file(title="Summer3", album=album, archived=True)
        response = self._retrieve_album(album.uuid)
        assert response.status_code == status.HTTP_200_OK
        assert self.result[to_camel_case(RetrieveFields.LIB_TRACKS_ARCHIVED_COUNT)] == 3
