#!/usr/bin/env python

from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_same_filename_so_suffixe_added(self):
        source_filename_without_extension = "sample"
        source_filename_extension = ".mp3"
        source_filename_with_extension = source_filename_without_extension + source_filename_extension
        self.post_lib_track_with_specific_sample(specific_sample_filename=source_filename_with_extension)
        track1 = self.saved_lib_track

        response = self.post_lib_track_with_specific_sample(specific_sample_filename=source_filename_with_extension)
        track2 = self.saved_lib_track

        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert track1.file_exists
        assert track1.filename == source_filename_with_extension
        assert track2.filename.startswith(source_filename_without_extension)
        assert track2.filename.endswith(source_filename_extension)
