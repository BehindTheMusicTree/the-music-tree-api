#!/usr/bin/env python
import pprint
import pytest
from rest_framework import status
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


@pytest.mark.django_db
class FlacTestCase(ApiViewTestCase):

    def test_noneThenNone(self):
        response = self.post_sample_track(sample_filename="noneThenNone.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.album.albumArtists.count() == 0

    def test_longest(self):
        response = self.post_sample_track(
            sample_filename="100CharAlbumArtistsName.flac")
        assert response.status_code == status.HTTP_201_CREATED
        pprint.pp(self.saved_track.album)
        assert self.saved_track.album.albumArtists.all().first().name == "4bTyH6zRq7Psk7Y9Pydmb4g" \
            + "TYs9VCVvehPANcaZHbviunfxtl5KwjgJQdUyvX9WKnsv0KAtwAiWmi739Fqt2KsGZi7F3Fn9AXPI3"
