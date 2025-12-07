from rest_framework import status

from api.serializer.model.uploaded_track.output.Fields import Fields as UploadedTrackOutputFields

from ..AllUploadedTracksMixinTestCase import AllUploadedTracksMixinTestCase


class TestCase(AllUploadedTracksMixinTestCase):

    def test_get_then_results(self):
        self.model_fixture_factory.create_uploaded_track_with_file(title="test")
        self.model_fixture_factory.create_uploaded_track_with_file(title="test2")

        response = self._get_all_uploaded_tracks_mixin()

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2

    def test_get_then_last_added_tracks_first(self):
        track1_title = self.model_fixture_factory.create_uploaded_track_with_file(title="test").title
        track2_title = self.model_fixture_factory.create_uploaded_track_with_file(title="test2").title
        track3_title = self.model_fixture_factory.create_uploaded_track_with_file(title="test3").title

        response = self._get_all_uploaded_tracks_mixin()

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 3
        uploaded_track_titles = [uploaded_track[UploadedTrackOutputFields.TITLE] for uploaded_track in self.results]
        assert uploaded_track_titles[0] == track3_title
        assert uploaded_track_titles[1] == track2_title
        assert uploaded_track_titles[2] == track1_title
