#!/usr/bin/env python
from rest_framework import status
from bodzify_api import settings
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TrackViewExtractTitleTestCase(ApiViewTestCase):

    def test_notProvidedThenSetFromFilename(self):
        filenameWithoutExtension = "notTooLongFilename"
        response = self.postSampleTrack(
            sampleFilename=filenameWithoutExtension + ".mp3", dataJson={})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.title == filenameWithoutExtension
