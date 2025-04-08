from datetime import timedelta

from django.utils import timezone

from bodzify_api.filtering.set.spotify.lib_track.SpotifyLibTrackFilterSet import SpotifyLibTrackFilterSet
from bodzify_api.filtering.set.spotify.lib_track.Fields import Fields
from bodzify_api.test.utils.AppTestCase import AppTestCase


class TestSpotifyLibTrackFilter(AppTestCase):
    def setUp(self):
        super().setUp()
        self.now = timezone.now()
        self.past = self.now - timedelta(days=5)
        self.future = self.now + timedelta(days=5)

        # Create test data
        self.artist1 = self.model_fixture_factory.create_spotify_artist(name="Artist 1")
        self.artist2 = self.model_fixture_factory.create_spotify_artist(name="Artist 2")

        self.track1 = self.model_fixture_factory.create_spotify_lib_track(
            name="Track 1",
            spotify_artists=[self.artist1],
            duration_ms=300000,  # 5 minutes
            popularity=80,
            explicit=True,
            last_synced_at=self.past,
            is_removed=False
        )

        self.track2 = self.model_fixture_factory.create_spotify_lib_track(
            name="Track 2",
            spotify_artists=[self.artist2],
            duration_ms=180000,  # 3 minutes
            popularity=60,
            explicit=False,
            last_synced_at=self.now,
            is_removed=False
        )

        self.track3 = self.model_fixture_factory.create_spotify_lib_track(
            name="Track 3",
            spotify_artists=[self.artist1],
            duration_ms=240000,  # 4 minutes
            popularity=40,
            explicit=True,
            last_synced_at=self.future,
            is_removed=True
        )

    def test_name_filter(self):
        filterset = SpotifyLibTrackFilterSet(
            {Fields.NAME_PUBLIC: "Track 1"},
            queryset=SpotifyLibTrackFilterSet.Meta.model.objects.all()
        )
        assert list(filterset.qs) == [self.track1]

    def test_album_artist_name_filter(self):
        filterset = SpotifyLibTrackFilterSet(
            {Fields.ALBUM_ARTIST_NAME: "Artist 1"},
            queryset=SpotifyLibTrackFilterSet.Meta.model.objects.all()
        )
        assert set(filterset.qs) == {self.track1, self.track3}

    def test_duration_sec_min_filter(self):
        filterset = SpotifyLibTrackFilterSet(
            {Fields.DURATION_SEC_MIN: 4},
            queryset=SpotifyLibTrackFilterSet.Meta.model.objects.all()
        )
        assert list(filterset.qs) == [self.track1]

    def test_duration_sec_max_filter(self):
        filterset = SpotifyLibTrackFilterSet(
            {Fields.DURATION_SEC_MAX: 3.5},
            queryset=SpotifyLibTrackFilterSet.Meta.model.objects.all()
        )
        assert list(filterset.qs) == [self.track2]

    def test_popularity_min_filter(self):
        filterset = SpotifyLibTrackFilterSet(
            {Fields.POPULARITY_MIN: 70},
            queryset=SpotifyLibTrackFilterSet.Meta.model.objects.all()
        )
        assert list(filterset.qs) == [self.track1]

    def test_popularity_max_filter(self):
        filterset = SpotifyLibTrackFilterSet(
            {Fields.POPULARITY_MAX: 50},
            queryset=SpotifyLibTrackFilterSet.Meta.model.objects.all()
        )
        assert list(filterset.qs) == [self.track3]

    def test_explicit_filter(self):
        filterset = SpotifyLibTrackFilterSet(
            {Fields.EXPLICIT: True},
            queryset=SpotifyLibTrackFilterSet.Meta.model.objects.all()
        )
        assert set(filterset.qs) == {self.track1, self.track3}

    def test_last_synced_at_filter(self):
        filterset = SpotifyLibTrackFilterSet(
            {Fields.LAST_SYNCED_AT: self.now.isoformat()},
            queryset=SpotifyLibTrackFilterSet.Meta.model.objects.all()
        )
        assert list(filterset.qs) == [self.track2]

    def test_last_synced_at_gt_filter(self):
        filterset = SpotifyLibTrackFilterSet(
            {Fields.LAST_SYNCED_AT_GT: self.now.isoformat()},
            queryset=SpotifyLibTrackFilterSet.Meta.model.objects.all()
        )
        assert list(filterset.qs) == [self.track3]

    def test_last_synced_at_lt_filter(self):
        filterset = SpotifyLibTrackFilterSet(
            {Fields.LAST_SYNCED_AT_LT: self.now.isoformat()},
            queryset=SpotifyLibTrackFilterSet.Meta.model.objects.all()
        )
        assert list(filterset.qs) == [self.track1]

    def test_last_synced_at_gte_filter(self):
        filterset = SpotifyLibTrackFilterSet(
            {Fields.LAST_SYNCED_AT_GTE: self.now.isoformat()},
            queryset=SpotifyLibTrackFilterSet.Meta.model.objects.all()
        )
        assert set(filterset.qs) == {self.track2, self.track3}

    def test_last_synced_at_lte_filter(self):
        filterset = SpotifyLibTrackFilterSet(
            {Fields.LAST_SYNCED_AT_LTE: self.now.isoformat()},
            queryset=SpotifyLibTrackFilterSet.Meta.model.objects.all()
        )
        assert set(filterset.qs) == {self.track1, self.track2}

    def test_is_removed_filter(self):
        filterset = SpotifyLibTrackFilterSet(
            {Fields.IS_REMOVED: True},
            queryset=SpotifyLibTrackFilterSet.Meta.model.objects.all()
        )
        assert list(filterset.qs) == [self.track3]

    def test_combined_filters(self):
        filterset = SpotifyLibTrackFilterSet(
            {
                Fields.ALBUM_ARTIST_NAME: "Artist 1",
                Fields.EXPLICIT: True,
                Fields.POPULARITY_MIN: 30,
                Fields.POPULARITY_MAX: 50
            },
            queryset=SpotifyLibTrackFilterSet.Meta.model.objects.all()
        )
        assert list(filterset.qs) == [self.track3]
