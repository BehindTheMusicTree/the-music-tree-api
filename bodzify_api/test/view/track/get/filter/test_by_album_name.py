
from rest_framework import status

from bodzify_api.serializer.schema.lib_track.output.Fields import Fields as LibTrackFields
from bodzify_api.serializer.schema.album.fields import Fields as AlbumFields
from bodzify_api.test.view.track.TrackTestCase import LibTrackTestCase
from bodzify_api.utils.utils import to_camel_case


class TestCase(LibTrackTestCase):

    def test_filter_empty_then_return_all(self):
        self.model_fixture_factory.create_lib_track_with_file(title="Life")
        self.model_fixture_factory.create_lib_track_with_file(title="Hey")
        response = self._get_lib_tracks(album_name='')
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 2

    def test_filter_not_empty_then_dont_return_track_with_no_album(self):
        self.model_fixture_factory.create_lib_track_with_file(title="Life")
        response = self._get_lib_tracks(album_name='jo')
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 0

    def test_an_album_name_contains_the_filter_then_return_its_track(self):
        album_life = self.model_fixture_factory.create_album(name="Life")
        track_life = self.model_fixture_factory.create_lib_track_with_file(title="Life", album=album_life)

        album_hey = self.model_fixture_factory.create_album(name="Hey")
        self.model_fixture_factory.create_lib_track_with_file(title="Hey", album=album_hey)

        response = self._get_lib_tracks(album_name='Lif')
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 1
        assert self.results[0][LibTrackFields.TITLE] == track_life.title

    def test_an_album_name_contains_the_filter_in_another_case_then_return_its_track(self):
        album_life = self.model_fixture_factory.create_album(name="LIfe")
        track_life = self.model_fixture_factory.create_lib_track_with_file(title="Life", album=album_life)

        album_hey = self.model_fixture_factory.create_album(name="Hey")
        self.model_fixture_factory.create_lib_track_with_file(title="Hey", album=album_hey)

        response = self._get_lib_tracks(album_name='Lif')
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 1
        assert self.results[0][LibTrackFields.TITLE] == track_life.title
