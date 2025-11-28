from datetime import timedelta

from django.utils import timezone
from rest_framework import status

from bodzify_api.serializer.model.spotify.lib_track.output.Fields import Fields as SpotifyLibTrackFields
from bodzify_api.test.view.spotify.lib_track.SpotifyLibTrackTestCase import SpotifyLibTrackTestCase


class TestCase(SpotifyLibTrackTestCase):
    def setUp(self):
        super().setUp()
        self.now = timezone.now()
        self.past = self.now - timedelta(days=5)
        self.future = self.now + timedelta(days=5)

    def test_last_synced_at_then_results(self):
        track1 = self.model_fixture_factory.create_spotify_lib_track(name="Track 1", last_synced_at=self.past)
        track2 = self.model_fixture_factory.create_spotify_lib_track(name="Track 2", last_synced_at=self.now)
        track3 = self.model_fixture_factory.create_spotify_lib_track(name="Track 3", last_synced_at=self.future)

        response = self._list_spotify_lib_tracks(last_synced_at=self.now.isoformat())

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[0][SpotifyLibTrackFields.NAME] == track2.name

    def test_last_synced_at_gt_then_results(self):
        track1 = self.model_fixture_factory.create_spotify_lib_track(name="Track 1", last_synced_at=self.past)
        track2 = self.model_fixture_factory.create_spotify_lib_track(name="Track 2", last_synced_at=self.now)
        track3 = self.model_fixture_factory.create_spotify_lib_track(name="Track 3", last_synced_at=self.future)

        response = self._list_spotify_lib_tracks(last_synced_at_gt=self.now.isoformat())

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[0][SpotifyLibTrackFields.NAME] == track3.name

    def test_last_synced_at_lt_then_results(self):
        track1 = self.model_fixture_factory.create_spotify_lib_track(name="Track 1", last_synced_at=self.past)
        track2 = self.model_fixture_factory.create_spotify_lib_track(name="Track 2", last_synced_at=self.now)
        track3 = self.model_fixture_factory.create_spotify_lib_track(name="Track 3", last_synced_at=self.future)

        response = self._list_spotify_lib_tracks(last_synced_at_lt=self.now.isoformat())

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[0][SpotifyLibTrackFields.NAME] == track1.name

    def test_last_synced_at_range_then_results(self):
        track1 = self.model_fixture_factory.create_spotify_lib_track(name="Track 1", last_synced_at=self.past)
        track2 = self.model_fixture_factory.create_spotify_lib_track(name="Track 2", last_synced_at=self.now)
        track3 = self.model_fixture_factory.create_spotify_lib_track(name="Track 3", last_synced_at=self.future)

        response = self._list_spotify_lib_tracks(
            last_synced_at_gte=self.past.isoformat(),
            last_synced_at_lte=self.now.isoformat()
        )

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
        names = {result[SpotifyLibTrackFields.NAME] for result in self.results}
        assert names == {track1.name, track2.name}
