from rest_framework import status

from bodzify_api.serializer.model.lib_track.output.Fields import \
    Fields as LibTrackFields
from bodzify_api.test.utils.field.filter.char.NullableFreeCharFilterTestCase import \
    NullableFreeCharFilterTestCase
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase, NullableFreeCharFilterTestCase):

    def test_empty_then_return_all(self):
        self.model_fixture_factory.create_lib_track_with_file(title="Life", language="en")
        self.model_fixture_factory.create_lib_track_with_file(title="Hey", language="fr")

        response = self._get_lib_tracks(language='')

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2

    def test_contains_in_another_case_then_results(self):
        track = self.model_fixture_factory.create_lib_track_with_file(title="LIfe", language="en")
        self.model_fixture_factory.create_lib_track_with_file(title="Hey", language="fr")

        response = self._get_lib_tracks(language='E')

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[0][LibTrackFields.TITLE] == track.title
