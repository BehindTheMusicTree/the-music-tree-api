#!/usr/bin/env python


from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_musicbrainz_link(self):
        response = self.post_lib_track_with_specific_sample("queen_duration_181.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.lib_track_saved.musicbrainz_recording.musicbrainz_link == (  # type: ignore
            "https://musicbrainz.org/recording/3604eb06-4bc2-4416-9b31-ceadae51bc70"
        )
