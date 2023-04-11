#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class LocationTestCase(ApiViewTestCase):

    def test_inLibrary(self):
        filename = "0001.wav"
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/" + filename,
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.file.name == self.testUserLibraryPathRelativeToMediaDir + filename
        assert self.doesTrackFilenameExistInTestUserLibrary(filename)