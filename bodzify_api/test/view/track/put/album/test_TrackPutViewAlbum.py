#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


class TrackPutViewTestCaseAlbum(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutDataAlbum']

    """
    The "albumName" field isn't specified. It must not be updated.
    """
    def test_trackPutAlbumUnchanged(self):
        data = {
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTARbJEK", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.album.name == "Dans La Légende"
        

    """
    Updating the album to the the one named "Absolution"
    """
    def test_trackPutAlbumMuse(self):
        data = {
            "albumName": "Absolution"
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTADDDDD", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.album.name == "Absolution"
        

    """
    The "albumName" field is empty. The updated value must be None.
    """
    def test_trackPutAlbumNone(self):
        data = {
            "language": None
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTADDDDD", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.language == None


    """
    Trying to update a track specifying the album albums name field and not the album field 
    should fail with a 400 error code.
    """
    def test_trackPutExtraField(self):

        data = {
            "title": "Somewhere I Belong",
            "albumAlbumsName": "Muse",
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDoihoihvTARbJEK", data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST