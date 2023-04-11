#!/usr/bin/env python
from rest_framework import status
from bodzify_api import settings
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TrackViewExtractTitleTestCase(ApiViewTestCase):

    def test_okWhenMaxLength(self):
        sample100CharLongCharName = ("3NyKu2inI7MA3DIRa78qLuowTOppybbfKx27gzOV7aiHJNcDTIDxSJJMNNY" +
                                     "s5B2xZk7Ka11zddHC6qlc4zjGYjboNkvbmLTd.mp3")
        response = self.postSampleTrack(
            sampleFilename=sample100CharLongCharName, dataJson={})
        assert response.status_code == status.HTTP_201_CREATED

    def test_errorWhenTooLong(self):
        sample101CharLongCharName = ("3NyKu2inI7MA3DIRa78qLuowTOppybbfKx27gzOV7aiHJNcDTIDxSJJMNNY" +
                                     "s5B2xZk7Ka11zddHC6qlc4zjGYjboNkvbmLTdv.mp3")
        response = self.postSampleTrack(
            sampleFilename=sample101CharLongCharName, dataJson={})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
