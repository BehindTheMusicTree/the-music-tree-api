#!/usr/bin/env python
from rest_framework import status
from bodzify_api import settings
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TrackViewExtractTitleTestCase(ApiViewTestCase):

    def test_notProvidedThenSetFromFilenameAsItIsNotTooLong(self):
        filenameWithoutExtension = "notTooLongFilename"
        response = self.postSampleTrack(
            sampleFilename=filenameWithoutExtension + ".mp3", dataJson={})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.title == filenameWithoutExtension

    def test_notProvidedAndFilenameTooLongSoRandomStringWithAppPrefix(self):
        response = self.postSampleTrack(sampleFilename="3NyKu2inI7MA3DIRa78qLuowTOppybbfKx27gzOV" +
                                        "7aiHJNcDTIDxSJJMNNYs5B2xZk7Ka11zddHC6qlc4zjGYjboNkvbmLT" +
                                        "dvDmXK.mp3",
                                        dataJson={})
        print(response.data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.title.startswith(
            settings.TRACK_GENERATED_TITLE_PREFIXE)
        assert len(self.savedTrack.title) == settings.TRACK_GENERATED_TITLE_LEN
