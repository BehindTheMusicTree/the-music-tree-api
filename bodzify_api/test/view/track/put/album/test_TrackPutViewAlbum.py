#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


class TrackPutViewTestCaseAlbum(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutDataAlbum']

    """
    The "albumName" field isn't specified. It must not be updated.
    """
    def test_trackPutAlbumUnchanged(self):
        data = {}
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTARbJEK", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.album.name == "Dans La Légende"
        

    """
    Updating the album with a string with the highest length allowed.
    """
    def test_trackPutAlbumLongestName(self):
        data = {
            "albumName": "a" * 100
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTARbJEK", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.album.name == "a" * 100
        

    """
    The "albumName" field is null. The updated value must be None.
    """
    def test_trackPutAlbumNone(self):
        data = {
            "albumName": None
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTADDKDK", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.album_id == None
