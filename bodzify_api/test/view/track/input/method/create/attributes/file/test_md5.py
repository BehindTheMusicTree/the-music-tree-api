#!/usr/bin/env python

from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase
from bodzify_api.utils import audio_metadata


class TestCase(TrackTestCase):

    def test_flac_md5_not_valid_then_corrected(self):
        response = self._post_lib_track_with_specific_sample("md5_not_valid.flac")
        assert response.status_code == status.HTTP_201_CREATED
        track_file = self.saved_lib_track.track_file
        assert track_file
        assert track_file.flac_md5_has_been_corrected
        assert audio_metadata.is_flac_file_md5_valid(track_file.file.path)

    def test_flac_md5_not_valid_and_corrupted_then_error(self):
        response = self._post_lib_track_with_specific_sample("md5_not_valid_and_corrupted.flac")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_flac_md5_is_valid(self):
        response = self._post_lib_track_with_specific_sample("md5_valid.flac")
        assert response.status_code == status.HTTP_201_CREATED
        track_file = self.saved_lib_track.track_file
        assert track_file
        assert not track_file.flac_md5_has_been_corrected

    def test_mp3_then_md5_check_is_none(self):
        response = self._post_lib_track_with_specific_sample("sample.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        track_file = self.saved_lib_track.track_file
        assert track_file
        assert not track_file.flac_md5_has_been_corrected
