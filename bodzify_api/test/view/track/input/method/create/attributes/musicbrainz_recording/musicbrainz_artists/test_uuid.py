#!/usr/bin/env python

import uuid

from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_one_then_ok(self):
        response = self.post_lib_track_with_specific_sample("queen_wearethechampions.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.musicbrainz_recording.musicbrainz_artists.all(  # type: ignore
        )[0].uuid == uuid.UUID("0383dadf-2a4e-4d10-a46a-e9e041da8eb3")

    def test_multiple_then_ok(self):
        response = self.post_lib_track_with_specific_sample("oostil_Juan Hansen.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        artists_uuids = [
            artist.uuid for artist in self.saved_lib_track.musicbrainz_recording.musicbrainz_artists.all()  # type: ignore
        ]
        assert uuid.UUID("d2fe3873-d123-4bea-a5ee-4340d865777c") in artists_uuids
        assert uuid.UUID("c4d2d3d2-8c93-499e-9c9e-571bf0d5cf29") in artists_uuids

    def test_same_artist_then_same_uuid(self):
        response = self.post_lib_track_with_specific_sample("queen_wearethechampions.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        first_track_musicbrainz_artist_uuid = \
            self.saved_lib_track.musicbrainz_recording.musicbrainz_artists.all()[0].uuid  # type: ignore

        response = self.post_lib_track_with_specific_sample("queen_showmustgoon.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        second_track_musicbrainz_artist_uuid = \
            self.saved_lib_track.musicbrainz_recording.musicbrainz_artists.all()[0].uuid  # type: ignore

        assert first_track_musicbrainz_artist_uuid == second_track_musicbrainz_artist_uuid
