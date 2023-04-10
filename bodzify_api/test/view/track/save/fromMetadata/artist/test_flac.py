#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.ApiViewTestCase import ApiViewTestCase


@pytest.mark.django_db
class FlacTestCase(ApiViewTestCase):
    
    def test_noneThenNone(self):
        response = self.postSampleTrack(sampleFilename="noneThenNone.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.artist == None
    
    def test_longest(self):
        response = self.postSampleTrack(sampleFilename="100CharArtistName.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.artist.name == "4bTyH6zRq7Psk7Y9Pydmb4gTYs9VCVvehPANcaZHbviunfxtl5Kwj" + \
            "gJQdUyvX9WKnsv0KAtwAiWmi739Fqt2KsGZi7F3Fn9AXPI3"
	
