from rest_framework import status

from api.serializer.model.album.detailed import Fields as RetrieveFields
from api.serializer.model.uploaded_track.output.simple.simple_without_album import Fields as UploadedTrackOutputFields
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.test.integration.view.album.AlbumTestCase import AlbumTestCase
from api.utils.data_transformer import to_camel_case


class TestCase(AlbumTestCase):

    def test_all_uploaded_tracks_with_positions_then_order_by_position_asc(self):
        album = self.model_fixture_factory.create_album(name="Chuck")
        uploaded_track_12th_position = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Love", album=album, track_number=12)
        uploaded_track_45th_position = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Loves", album=album, track_number=45)
        uploaded_track_1st_position = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Lovdddde", album=album, track_number=1)

        response = self._retrieve_album(uuid=album.uuid)

        assert response.status_code == status.HTTP_200_OK
        result_tracks = self.result[to_camel_case(RetrieveFields.UPLOADED_TRACKS_NOT_ARCHIVED_SORTED_PUBLIC)]

        assert result_tracks[0][to_camel_case(UploadedTrackOutputFields.TITLE)] == uploaded_track_1st_position.title
        assert result_tracks[1][to_camel_case(UploadedTrackOutputFields.TITLE)] == uploaded_track_12th_position.title
        assert result_tracks[2][to_camel_case(UploadedTrackOutputFields.TITLE)] == uploaded_track_45th_position.title

    def test_some_uploaded_tracks_with_positions_then_order_by_position_asc_then_those_with_no_position_by_title_asc(
            self):
        album = self.model_fixture_factory.create_album(name="Chuck")
        uploaded_track_112th_position = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Love", album=album, track_number=112)
        uploaded_track_4th_position = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Loves", album=album, track_number=2)
        uploaded_track_no_position_3 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Lovdddde", album=album)
        uploaded_track_no_position_4 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Movee", album=album)
        uploaded_track_no_position_2 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Jooove", album=album)
        uploaded_track_no_position_1 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Ave", album=album)

        response = self._retrieve_album(uuid=album.uuid)

        assert response.status_code == status.HTTP_200_OK
        result_tracks = self.result[to_camel_case(RetrieveFields.UPLOADED_TRACKS_NOT_ARCHIVED_SORTED_PUBLIC)]
        assert result_tracks[0][to_camel_case(UploadedTrackOutputFields.TITLE)] == uploaded_track_4th_position.title
        assert result_tracks[1][to_camel_case(UploadedTrackOutputFields.TITLE)] == uploaded_track_112th_position.title
        assert result_tracks[2][to_camel_case(UploadedTrackOutputFields.TITLE)] == uploaded_track_no_position_1.title
        assert result_tracks[3][to_camel_case(UploadedTrackOutputFields.TITLE)] == uploaded_track_no_position_2.title
        assert result_tracks[4][to_camel_case(UploadedTrackOutputFields.TITLE)] == uploaded_track_no_position_3.title
        assert result_tracks[5][to_camel_case(UploadedTrackOutputFields.TITLE)] == uploaded_track_no_position_4.title

    def test_duration(self):
        album = self.model_fixture_factory.create_album(name="Chuck")
        self.model_fixture_factory.create_uploaded_track_with_file(
            title='ciline', album=album, test_uploaded_track_filename=UploadedTrackTestFilename.DURATION_277S_MP3)
        self.model_fixture_factory.create_uploaded_track_with_file(
            title='tokyo', album=album, test_uploaded_track_filename=UploadedTrackTestFilename.DURATION_472S_WAV)

        response = self._retrieve_album(album.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.result[to_camel_case(RetrieveFields.DURATION_IN_SEC)] == 277 + 472

    def test_count(self):
        album = self.model_fixture_factory.create_album(name="Chuck")
        self.model_fixture_factory.create_uploaded_track_with_file(title="In Too Deep", album=album)
        self.model_fixture_factory.create_uploaded_track_with_file(title="Summer", album=album)

        response = self._retrieve_album(album.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.result[to_camel_case(RetrieveFields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC)] == 2

    def test_archived_count(self):
        album = self.model_fixture_factory.create_album(name="Chuck")
        self.model_fixture_factory.create_uploaded_track_with_file(title="In Too Deep", album=album)
        self.model_fixture_factory.create_uploaded_track_with_file(title="Summer", album=album, archived=True)
        self.model_fixture_factory.create_uploaded_track_with_file(title="Summer2", album=album, archived=True)
        self.model_fixture_factory.create_uploaded_track_with_file(title="Summer3", album=album, archived=True)

        response = self._retrieve_album(album.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.result[to_camel_case(RetrieveFields.UPLOADED_TRACKS_ARCHIVED_COUNT_PUBLIC)] == 3
