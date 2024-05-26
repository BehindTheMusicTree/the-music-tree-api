#!/usr/bin/env python

from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase
import bodzify_api.audiometadata as audiometadata


class TestCase(TrackTestCase):

    def test_flac_md5_not_valid_then_corrected(self):
        response = self.post_lib_track_with_specific_sample("fingerprint.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.track_file.has_flac_md5_been_corrected is True
        assert audiometadata.is_flac_file_md5_valid(
            self.saved_lib_track.track_file.file.path) is True
