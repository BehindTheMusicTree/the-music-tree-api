#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


class TrackPutViewTestCaseExtraField(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutDataAlbumNotSet']


    """
    Trying to update a track specifying the album artists name field and not the album field 
    should fail with a 400 error code.
    """
    def test_trackPutExtraField(self):

        data = {
            "title": "Somewhere I Belong",
            "albumArtistsName": "Muse",
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDoihoihvTARbJEK", data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
