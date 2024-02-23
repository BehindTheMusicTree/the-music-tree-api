#!/usr/bin/env python

import pprint

import pytest
from rest_framework import status

from bodzify_api.test.view.track.input.source.file_metadata.AttributeFromFileMetadataTestCase import \
    AttributeFromFileMetadataTestCase


@pytest.mark.django_db
class TestCase(AttributeFromFileMetadataTestCase):

    def test_none_then_none(self):
        response = self.post_sample_lib_track(sample_filename="none.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.album.album_artists.count() == 0

    def test_longest(self):
        response = self.post_sample_lib_track(sample_filename="100_char_album_artists_name.flac")
        assert response.status_code == status.HTTP_201_CREATED
        pprint.pp(self.saved_lib_track.album)
        assert self.saved_lib_track.album.album_artists.all().first().name == "4bTyH6zRq7Psk7Y9Pydmb4g" \
            + "TYs9VCVvehPANcaZHbviunfxtl5KwjgJQdUyvX9WKnsv0KAtwAiWmi739Fqt2KsGZi7F3Fn9AXPI3"
