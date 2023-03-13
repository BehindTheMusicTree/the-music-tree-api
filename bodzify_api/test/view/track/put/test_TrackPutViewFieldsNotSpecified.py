#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


class TrackPutViewTestCaseExtraField(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutDataAlbumNotSet']


    """
    Not specifying fields must not update them.
    """
    def test_trackPutFieldsNotSpecified(self):

        data = {
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.title == "Luz De Luna"
        assert self.savedTrack.album_id == "Lsji85mqisjdjf881DJDHD"
        assert self.savedTrack.artist_id == "Lsji85mqisjdjf88LKCFG6"
        assert self.savedTrack.genre_id == "LsjdqoqzpsdojEjGHGH"
        assert self.savedTrack.rating == "8"
        assert self.savedTrack.language == "Latin"