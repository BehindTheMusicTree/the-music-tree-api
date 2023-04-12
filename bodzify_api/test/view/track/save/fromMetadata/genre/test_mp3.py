#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


@pytest.mark.django_db
class TestCase(ApiViewTestCase):
    
    def test_noneThenNone(self):
        response = self.postSampleTrack(sampleFilename="noneThenNone.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.genre == None
    
    def test_longest(self):
        response = self.postSampleTrack(sampleFilename="100CharGenreName.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.genre.name == "4bTyH6zRq7Psk7Y9Pydmb4gTYs9VCVvehPANcaZHbviunfxtl5Kwj" + \
            "gJQdUyvX9WKnsv0KAtwAiWmi739Fqt2KsGZi7F3Fn9AXPI3"
	
	
