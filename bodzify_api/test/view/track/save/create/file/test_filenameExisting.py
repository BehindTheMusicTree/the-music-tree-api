#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_sameFilenameSoSuffixeAdded(self):
        sourceFilenameWithoutExtension = "sample"
        sourceFilenameExtension = ".mp3"
        sourceFilenameWithExtension = sourceFilenameWithoutExtension + sourceFilenameExtension
        self.post_sample_track(sample_filename=sourceFilenameWithExtension)
        track1 = self.saved_track
        response = self.post_sample_track(sample_filename=sourceFilenameWithExtension)
        track2 = self.saved_track
        assert response.status_code == status.HTTP_201_CREATED
        assert track1.fileExists
        assert track1.filename == sourceFilenameWithExtension
        assert track2.filename.startswith(sourceFilenameWithoutExtension)
        assert track2.filename.endswith(sourceFilenameExtension)
        
