#!/usr/bin/env python

from rest_framework import status
from bodzify_api.test.AppTestCase import AppTestCase
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_not_povided_then_set_from_filename_without_dots(self):
        response = self.post_lib_track_with_generic_sample_no_tags()
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.title == self.LIB_TRACK_GENERIC_SAMPLES_FILENAMES_WITHOUT_EXTENSION.TAGS_NONE

    def test_not_povided_then_set_from_filename_with_dots(self):
        filename_without_extension = "dot.in.filename"
        response = self.post_lib_track_with_specific_sample(filename_without_extension + ".mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.title == filename_without_extension
