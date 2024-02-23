#!/usr/bin/env python

import pytest
from rest_framework import status

from bodzify_api.test.view.track.input.source.file_metadata.AttributeFromFileMetadataTestCase import \
    AttributeFromFileMetadataTestCase


@pytest.mark.django_db
class TestCase(AttributeFromFileMetadataTestCase):

    def test_none_then_none(self):
        response = self.post_sample_lib_track(sample_filename="none.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.genre == None

    def test_longest(self):
        response = self.post_sample_lib_track(
            sample_filename="50_char_genre_name.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.genre.name == "4bTyH6zRq7Psk7Y9Pydmb4gTYs9VCVvehPANcaZHbviunfxtl5"
