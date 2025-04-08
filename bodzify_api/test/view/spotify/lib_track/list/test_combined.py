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

    def test_name_and_artist_name_then_results(self):
        artist1 = self.model_fixture_factory.create_spotify_artist(name="Artist 1")
        artist2 = self.model_fixture_factory.create_spotify_artist(name="Artist 2")
        track1 = self.model_fixture_factory.create_spotify_lib_track(
            name="Track 1",
            spotify_artists=[artist1]
        )
        track2 = self.model_fixture_factory.create_spotify_lib_track(
            name="Track 2",
            spotify_artists=[artist2]
        )
        track3 = self.model_fixture_factory.create_spotify_lib_track(
            name="Track 3",
            spotify_artists=[artist1]
        )

        response = self._list_spotify_lib_tracks(
            name="Track",
            album_artist_name="Artist 1"
        )

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
        names = {result[SpotifyLibTrackFields.NAME] for result in self.results}
        assert names == {track1.name, track3.name}

    def test_duration_and_popularity_then_results(self):
        track1 = self.model_fixture_factory.create_spotify_lib_track(
            name="Track 1",
            duration_ms=300000,  # 5 minutes
            popularity=80
        )
        track2 = self.model_fixture_factory.create_spotify_lib_track(
            name="Track 2",
            duration_ms=180000,  # 3 minutes
            popularity=60
        )
        track3 = self.model_fixture_factory.create_spotify_lib_track(
            name="Track 3",
            duration_ms=240000,  # 4 minutes
            popularity=40
        )

        response = self._list_spotify_lib_tracks(
            duration_sec_min=3.5,
            duration_sec_max=4.5,
            popularity_min=50,
            popularity_max=70
        )

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[0][SpotifyLibTrackFields.NAME] == track2.name

    def test_explicit_and_last_synced_then_results(self):
        track1 = self.model_fixture_factory.create_spotify_lib_track(
            name="Track 1",
            explicit=True,
            last_synced_at=self.past
        )
        track2 = self.model_fixture_factory.create_spotify_lib_track(
            name="Track 2",
            explicit=False,
            last_synced_at=self.now
        )
        track3 = self.model_fixture_factory.create_spotify_lib_track(
            name="Track 3",
            explicit=True,
            last_synced_at=self.future
        )

        response = self._list_spotify_lib_tracks(
            explicit=True,
            last_synced_at_gte=self.past.isoformat(),
            last_synced_at_lte=self.now.isoformat()
        )

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[0][SpotifyLibTrackFields.NAME] == track1.name

    def test_all_filters_then_results(self):
        artist1 = self.model_fixture_factory.create_spotify_artist(name="Artist 1")
        artist2 = self.model_fixture_factory.create_spotify_artist(name="Artist 2")
        track1 = self.model_fixture_factory.create_spotify_lib_track(
            name="Track 1",
            spotify_artists=[artist1],
            duration_ms=300000,  # 5 minutes
            popularity=80,
            explicit=True,
            last_synced_at=self.past,
            is_removed=False
        )
        track2 = self.model_fixture_factory.create_spotify_lib_track(
            name="Track 2",
            spotify_artists=[artist2],
            duration_ms=180000,  # 3 minutes
            popularity=60,
            explicit=False,
            last_synced_at=self.now,
            is_removed=False
        )
        track3 = self.model_fixture_factory.create_spotify_lib_track(
            name="Track 3",
            spotify_artists=[artist1],
            duration_ms=240000,  # 4 minutes
            popularity=40,
            explicit=True,
            last_synced_at=self.future,
            is_removed=True
        )

        response = self._list_spotify_lib_tracks(
            name="Track",
            album_artist_name="Artist 1",
            duration_sec_min=3.5,
            duration_sec_max=4.5,
            popularity_min=30,
            popularity_max=50,
            explicit=True,
            last_synced_at_gte=self.past.isoformat(),
            last_synced_at_lte=self.future.isoformat(),
            is_removed=True
        )

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[0][SpotifyLibTrackFields.NAME] == track3.name
