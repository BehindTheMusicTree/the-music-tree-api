from rest_framework import status

from bodzify_api.serializer.model.lib_track.output.Fields import Fields as LibTrackFields
from bodzify_api.test.utils.field.filter.char.NullableCharFilterTestCase import NullableCharFilterTestCase
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase, NullableCharFilterTestCase):

    def test_not_provided_then_results(self):
        self.model_fixture_factory.create_lib_track_with_file(title="Life")
        self.model_fixture_factory.create_lib_track_with_file(title="Hey")
        genre = self.model_fixture_factory.create_genre(name="Rock")
        self.model_fixture_factory.create_lib_track_with_file(title="Hey", genre=genre)

        response = self._get_lib_tracks()

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 3

    def test_empty_then_results(self):
        self.model_fixture_factory.create_lib_track_with_file(title="Life")
        self.model_fixture_factory.create_lib_track_with_file(title="Hey")
        genre = self.model_fixture_factory.create_genre(name="Rock")
        self.model_fixture_factory.create_lib_track_with_file(title="Hey", genre=genre)

        response = self._get_lib_tracks(genre_name='')

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2

    def test_contains_in_another_case_then_results(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        track_life = self.model_fixture_factory.create_lib_track_with_file(title="Life", genre=genre_rock)

        genre_punk = self.model_fixture_factory.create_genre(name="Punk")
        self.model_fixture_factory.create_lib_track_with_file(title="Hey", genre=genre_punk)

        response = self._get_lib_tracks(genre_name='RoC')

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[0][LibTrackFields.TITLE] == track_life.title
