#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


class TrackViewArtistTestCase(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutArtistData']

    """
    The "artistName" field isn't specified. It must not be updated.
    """
    def test_trackPutArtistUnchanged(self):
        data = {
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTARbJEK", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.artist.name == "PNL"
        

    """
    Updating the artist to the the one named "Muse"
    """
    def test_trackPutArtistMuse(self):
        data = {
            "artistName": "Muse"
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTADDDDD", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.artist.name == "Muse"
        

    """
    The "artistName" field is empty. The updated value must be None.
    """
    def test_trackPutArtistNone(self):
        data = {
            "artistName": None
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTADDDDD", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.artist_id == None
