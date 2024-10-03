#!/usr/bin/env python

from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_musicbrainz_link(self):
        response = self.post_lib_track_with_specific_sample("queen_wearethechampions.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.lib_track_saved.musicbrainz_recording.musicbrainz_artists.all()[0].musicbrainz_link == (  # type: ignore
            "https://musicbrainz.org/artist/0383dadf-2a4e-4d10-a46a-e9e041da8eb3"
        )
