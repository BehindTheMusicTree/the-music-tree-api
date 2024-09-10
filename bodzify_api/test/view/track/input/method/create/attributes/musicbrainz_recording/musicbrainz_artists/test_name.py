#!/usr/bin/env python

from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_one_then_ok(self):
        response = self.post_lib_track_with_specific_sample("queen_wearethechampions.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.musicbrainz_recording.musicbrainz_artists.all()[0].name == "Queen"  # type: ignore

    def test_multiple_then_ok(self):
        response = self.post_lib_track_with_specific_sample("oostil_Juan Hansen.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        artists_names = [
            artist.name for artist in self.saved_lib_track.musicbrainz_recording.musicbrainz_artists.all()  # type: ignore
        ]
        assert "Øostil" in artists_names
        assert "Juan Hansen" in artists_names
