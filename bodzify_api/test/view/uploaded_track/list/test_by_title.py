from rest_framework import status

from bodzify_api.serializer.model.uploaded_track.output.Fields import Fields as LibTrackFields
from bodzify_api.test.utils.field.filter.char.NotNullableFreeCharFilterTestCase import NotNullableFreeCharFilterTestCase
from bodzify_api.test.view.uploaded_track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase, NotNullableFreeCharFilterTestCase):

    def test_not_provided_then_results(self):
        self.model_fixture_factory.create_uploaded_track_with_file(title="Life")
        self.model_fixture_factory.create_uploaded_track_with_file(title="Hey")

        response = self._list_uploaded_tracks()

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2

    def test_empty_then_400_bad_request(self):
        self.model_fixture_factory.create_uploaded_track_with_file(title="Life")
        self.model_fixture_factory.create_uploaded_track_with_file(title="Hey")

        response = self._list_uploaded_tracks(title='')

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2

    def test_contains_in_another_case_then_results(self):
        track = self.model_fixture_factory.create_uploaded_track_with_file(title="LIfe")
        self.model_fixture_factory.create_uploaded_track_with_file(title="Hey")

        response = self._list_uploaded_tracks(title='Lif')

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[0][LibTrackFields.TITLE] == track.title
