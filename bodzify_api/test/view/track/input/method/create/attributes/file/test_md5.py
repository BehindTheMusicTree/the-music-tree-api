#!/usr/bin/env python

from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase
import bodzify_api.utils.audiometadata as audiometadata


class TestCase(TrackTestCase):

    def test_flac_md5_not_valid_then_corrected(self):
        response = self.post_lib_track_with_specific_sample("md5_not_valid.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.track_file.has_flac_md5_been_corrected is True
        assert audiometadata.is_flac_file_md5_valid(
            self.saved_lib_track.track_file.file.path) is True

    def test_flac_md5_not_valid_and_corrupted_then_error(self):
        response = self.post_lib_track_with_specific_sample("md5_not_valid_and_corrupted.flac")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_flac_md5_is_valid(self):
        response = self.post_lib_track_with_specific_sample("md5_valid.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.track_file.has_flac_md5_been_corrected is False

    def test_mp3_then_md5_check_is_none(self):
        response = self.post_lib_track_with_specific_sample("sample.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.track_file.has_flac_md5_been_corrected is None
