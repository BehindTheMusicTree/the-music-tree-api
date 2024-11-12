from rest_framework import status

from bodzify_api.serializer.schema.lib_track.output.Fields import Fields as LibTrackFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.utils import data_transformer


class TestCase(LibTrackTestCase):

    def test_filter_empty_then_return_all(self):
        self.model_fixture_factory.create_lib_track_with_file(title="Life")
        self.model_fixture_factory.create_lib_track_with_file(title="Hey")
        response = self._get_lib_tracks(title='')
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 2

    def test_a_title_contains_the_filter_then_return_it(self):
        track = self.model_fixture_factory.create_lib_track_with_file(title="Life")
        self.model_fixture_factory.create_lib_track_with_file(title="Hey")
        response = self._get_lib_tracks(title='Lif')
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 1
        assert self.results[0][data_transformer.to_camel_case(LibTrackFields.TITLE)] == track.title

    def test_a_title_contains_the_filter_in_another_case_then_return_it(self):
        track = self.model_fixture_factory.create_lib_track_with_file(title="LIfe")
        self.model_fixture_factory.create_lib_track_with_file(title="Hey")
        response = self._get_lib_tracks(title='Lif')
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 1
        assert self.results[0][data_transformer.to_camel_case(LibTrackFields.TITLE)] == track.title
