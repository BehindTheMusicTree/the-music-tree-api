from rest_framework import status

from bodzify_api.serializer.model.uploaded_track.output.Fields import Fields as LibTrackFields
from bodzify_api.test.utils.field.filter.char.NullableCharFilterTestCase import NullableCharFilterTestCase
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase, NullableCharFilterTestCase):

    def test_not_provided_then_results(self):
        track = self.model_fixture_factory.create_uploaded_track_with_file(title="Life", language="en")
        self.model_fixture_factory.create_uploaded_track_with_file(title="Hey", language="fr")

        response = self._list_uploaded_tracks()

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2

    def test_empty_then_results(self):
        self.model_fixture_factory.create_uploaded_track_with_file(title="Life", language="en")
        self.model_fixture_factory.create_uploaded_track_with_file(title="Hey", language="fr")
        self.model_fixture_factory.create_uploaded_track_with_file(title="Hey haa")

        response = self._list_uploaded_tracks(language='')

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1

    def test_contains_in_another_case_then_results(self):
        track = self.model_fixture_factory.create_uploaded_track_with_file(title="LIfe", language="en")
        self.model_fixture_factory.create_uploaded_track_with_file(title="Hey", language="fr")

        response = self._list_uploaded_tracks(language='E')

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[0][LibTrackFields.TITLE] == track.title
