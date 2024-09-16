#!/usr/bin/env python

import uuid

from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_not_found_then_none(self):
        response = self.post_lib_track_with_specific_sample("Y do i - Carmina Burana Remix - 7m53_not_found.wav")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.musicbrainz_recording is None

    def test_drown_7m21_mp3_then_ok(self):
        response = self.post_lib_track_with_specific_sample("oostil - drown (massano remix) - 7m21.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.musicbrainz_recording.uuid == uuid.UUID(  # type: ignore
            "4a45b00b-273d-40ed-9ecd-42f387f59c22")

    def test_totaleclipe_5m35_flac_then_ok(self):
        response = self.post_lib_track_with_specific_sample("Bonnie Tyler - Total Eclipse of the Heart - 5m35.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.musicbrainz_recording.uuid == uuid.UUID(  # type: ignore
            "9f3c3b61-41a6-4bb9-a49c-33606f536784")

    def test_different_format_but_same_musicbrainz_recording(self):
        response = self.post_lib_track_with_specific_sample("oostil - drown (massano remix) - 7m20.flac")
        assert response.status_code == status.HTTP_201_CREATED
        flac_recording_id = self.saved_lib_track.musicbrainz_recording.uuid  # type: ignore

        response = self.post_lib_track_with_specific_sample("oostil - drown (massano remix) - 7m21.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.musicbrainz_recording.uuid == flac_recording_id  # type: ignore
