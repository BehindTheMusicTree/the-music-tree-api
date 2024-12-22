from rest_framework import status

from bodzify_api.utils.data_transformer import to_camel_case

from ..AllLibTracksMixinTestCase import AllLibTracksMixinTestCase

from bodzify_api.serializer.schema.model.lib_track.output.Fields import Fields as LibTrackOutputFields


class TestCase(AllLibTracksMixinTestCase):

    def test_get_then_results(self):
        self.model_fixture_factory.create_lib_track_with_file(title="test")
        self.model_fixture_factory.create_lib_track_with_file(title="test2")

        response = self._get_all_lib_tracks_mixin()

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2

    def test_get_then_last_added_tracks_first(self):
        track1_title = self.model_fixture_factory.create_lib_track_with_file(title="test").title
        track2_title = self.model_fixture_factory.create_lib_track_with_file(title="test2").title
        track3_title = self.model_fixture_factory.create_lib_track_with_file(title="test3").title

        response = self._get_all_lib_tracks_mixin()

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 3
        lib_track_titles = [lib_track[LibTrackOutputFields.TITLE] for lib_track in self.results]
        assert lib_track_titles[0] == track3_title
        assert lib_track_titles[1] == track2_title
        assert lib_track_titles[2] == track1_title
