#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


@pytest.mark.django_db
class Mp3TestCase(TrackViewTestCase):

    def test_noneThenNone(self):
        response = self.postSampleTrack(sampleFilename="noneThenNone.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.album.albumArtists.count() == 0

    def test_longest(self):
        response = self.postSampleTrack(
            sampleFilename="100CharAlbumArtistsName.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.album.albumArtists.all().first().name == "4bTyH6zRq7Psk7Y9Pydmb4g" \
            + "TYs9VCVvehPANcaZHbviunfxtl5KwjgJQdUyvX9WKnsv0KAtwAiWmi739Fqt2KsGZi7F3Fn9AXPI3"
