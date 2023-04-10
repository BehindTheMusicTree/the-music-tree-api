#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.ApiViewTestCase import ApiViewTestCase


@pytest.mark.django_db
class WavTestCase(ApiViewTestCase):
    
    def test_noneThenFilename(self):
        filename = "noneThenFilename"
        response = self.postSampleTrack(sampleFilename=filename + ".wav")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.title == filename
    
    def test_longest(self):
        response = self.postSampleTrack(sampleFilename="100CharTitle.wav")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.title == "4bTyH6zRq7Psk7Y9Pydmb4gTYs9VCVvehPANcaZHbviunfxtl5Kwj" + \
            "gJQdUyvX9WKnsv0KAtwAiWmi739Fqt2KsGZi7F3Fn9AXPI3"
	
