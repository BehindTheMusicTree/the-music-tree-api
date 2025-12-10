from rest_framework import status

from api.serializer.model.track.output.Fields import Fields as TrackFields
from api.test.utils.field.filter.char.NotNullableFreeCharFilterTestCase import NotNullableFreeCharFilterTestCase
from api.test.integration.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase, NotNullableFreeCharFilterTestCase):

    def test_not_provided_then_results(self):
        self.model_fixture_factory.create_track_with_file(title="Life")
        self.model_fixture_factory.create_track_with_file(title="Hey")

        response = self._list_tracks()

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2

    def test_empty_then_400_bad_request(self):
        self.model_fixture_factory.create_track_with_file(title="Life")
        self.model_fixture_factory.create_track_with_file(title="Hey")

        response = self._list_tracks(title='')

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2

    def test_contains_in_another_case_then_results(self):
        track = self.model_fixture_factory.create_track_with_file(title="LIfe")
        self.model_fixture_factory.create_track_with_file(title="Hey")

        response = self._list_tracks(title='Lif')

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[0][TrackFields.TITLE] == track.title
