from rest_framework import status

from api.serializer.model.track.output.Fields import Fields as TrackOutputFields

from ..AllTracksMixinTestCase import AllTracksMixinTestCase


class TestCase(AllTracksMixinTestCase):

    def test_get_then_results(self):
        self.model_fixture_factory.create_track_with_file(title="test")
        self.model_fixture_factory.create_track_with_file(title="test2")

        response = self._get_all_tracks_mixin()

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2

    def test_get_then_last_added_tracks_first(self):
        track1_title = self.model_fixture_factory.create_track_with_file(title="test").title
        track2_title = self.model_fixture_factory.create_track_with_file(title="test2").title
        track3_title = self.model_fixture_factory.create_track_with_file(title="test3").title

        response = self._get_all_tracks_mixin()

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 3
        track_titles = [track[TrackOutputFields.TITLE] for track in self.results]
        assert track_titles[0] == track3_title
        assert track_titles[1] == track2_title
        assert track_titles[2] == track1_title
