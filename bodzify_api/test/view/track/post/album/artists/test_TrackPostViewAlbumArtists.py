#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


@pytest.mark.django_db
class TrackPostViewAlbumArtistsTestCase(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/album/artists/sample/"

    """
    Non existing album artists "Jacky" and "Michelle".
    """
    def test_trackPostAlbumArtistsNonExisting(self):
        self._loginAndPostSampleTrack("sample with tags.wav")
        assert self.savedTrack.album.albumArtists.count() == 2
        assert self.savedTrack.album.albumArtists.filter(
                user=self.testUser, name="Jacky").exists()
        assert self.savedTrack.album.albumArtists.filter(
                user=self.testUser, name="Michelle").exists()


    """
    The posted album has album artists but no album. The resulting track should have no album
    linked.
    """
    def test_trackPostAlbumArtistsWithoutAlbum(self):
        response = self._loginAndPostSampleTrack("with album artists and no album.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.album is None
