#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_sameFilenameSoSuffixeAdded(self):
        sourcefilename_without_extension = "sample"
        sourceFilenameExtension = ".mp3"
        sourcefilename_with_extension = sourcefilename_without_extension + sourceFilenameExtension
        self.post_sample_track(sample_filename=sourcefilename_with_extension)
        track1 = self.saved_track
        response = self.post_sample_track(sample_filename=sourcefilename_with_extension)
        track2 = self.saved_track
        assert response.status_code == status.HTTP_201_CREATED
        assert track1.fileExists
        assert track1.filename == sourcefilename_with_extension
        assert track2.filename.startswith(sourcefilename_without_extension)
        assert track2.filename.endswith(sourceFilenameExtension)
        
