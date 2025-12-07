from rest_framework import status

from api.serializer.model.uploaded_track.output.Fields import Fields as UploadedTrackFields
from api.test.utils.field.filter.char.NullableCharFilterTestCase import NullableCharFilterTestCase
from api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase, NullableCharFilterTestCase):

    def test_not_provided_then_results(self):
        self.model_fixture_factory.create_uploaded_track_with_file(title="Life")
        self.model_fixture_factory.create_uploaded_track_with_file(title="Hey")

        response = self._list_uploaded_tracks()

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2

    def test_empty_then_results(self):
        self.model_fixture_factory.create_uploaded_track_with_file(title="Life")
        self.model_fixture_factory.create_uploaded_track_with_file(title="Hey")
        artist = self.model_fixture_factory.create_artist(name="John")
        self.model_fixture_factory.create_uploaded_track_with_file(title="Hey", artists=[artist])

        response = self._list_uploaded_tracks(artists_name='')

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2

    def test_filter_not_empty_then_dont_return_track_with_no_artist(self):
        self.model_fixture_factory.create_uploaded_track_with_file(title="Life")

        response = self._list_uploaded_tracks(artists_name='jo')

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 0

    def test_contains_in_another_case_then_results(self):
        artist_john = self.model_fixture_factory.create_artist(name="John")
        track_life = self.model_fixture_factory.create_uploaded_track_with_file(title="Life", artists=[artist_john])

        artist_mitch = self.model_fixture_factory.create_artist(name="Mitch")
        self.model_fixture_factory.create_uploaded_track_with_file(title="Hey", artists=[artist_mitch])

        response = self._list_uploaded_tracks(artists_name='JoH')

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[0][UploadedTrackFields.TITLE] == track_life.title
