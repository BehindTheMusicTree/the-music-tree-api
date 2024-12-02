from rest_framework import status

from bodzify_api.serializer.schema.model.lib_track.output.Fields import Fields as LibTrackFields
from bodzify_api.test.get_filters.char.NullableFreeCharFilterTestCase import NullableFreeCharFilterTestCase
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase, NullableFreeCharFilterTestCase):

    def test_empty_then_return_all(self):
        self.model_fixture_factory.create_lib_track_with_file(title="Life")
        self.model_fixture_factory.create_lib_track_with_file(title="Hey")
        response = self._get_lib_tracks(genre_name='')
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2

    def test_filter_not_empty_then_dont_return_track_with_no_genre(self):
        self.model_fixture_factory.create_lib_track_with_file(title="Life")
        response = self._get_lib_tracks(genre_name='jo')
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 0

    def test_contains_in_another_case_then_results(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        track_life = self.model_fixture_factory.create_lib_track_with_file(title="Life", genre=genre_rock)

        genre_punk = self.model_fixture_factory.create_genre(name="Punk")
        self.model_fixture_factory.create_lib_track_with_file(title="Hey", genre=genre_punk)

        response = self._get_lib_tracks(genre_name='RoC')
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[0][LibTrackFields.TITLE] == track_life.title
