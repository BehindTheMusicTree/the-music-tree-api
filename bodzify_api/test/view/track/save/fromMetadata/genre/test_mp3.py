#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


@pytest.mark.django_db
class TestCase(ApiViewTestCase):
    
    def test_noneThenNone(self):
        response = self.post_sample_track(sample_filename="none_then_none.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.genre == None
    
    def test_longest(self):
        response = self.post_sample_track(sample_filename="50_char_genre_name.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.genre.name == "4bTyH6zRq7Psk7Y9Pydmb4gTYs9VCVvehPANcaZHbviunfxtl5"
	
	
