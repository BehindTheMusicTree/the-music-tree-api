#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


@pytest.mark.django_db
class WavTestCase(TrackViewTestCase):
    
    def test_noneThenNone(self):
        response = self.postSampleTrack(sampleFilename="noneThenNone.wav")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.album == None
    
    def test_longest(self):
        response = self.postSampleTrack(sampleFilename="100CharAlbumName.wav")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.album.name == "4bTyH6zRq7Psk7Y9Pydmb4gTYs9VCVvehPANcaZHbviunfxtl5Kwj" + \
            "gJQdUyvX9WKnsv0KAtwAiWmi739Fqt2KsGZi7F3Fn9AXPI3"
	
	
