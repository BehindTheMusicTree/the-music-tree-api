#!/usr/bin/env python
import pprint
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


class TrackPutViewTestCaseAlbumArtists(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutDataAlbumArtists']

    # """
    # The "albumArtistsName" field isn't specified. It must not be updated.
    # """
    # def test_trackPutAlbumArtistsUnchanged(self):
    #     data = {
    #         "albumName": "Chuck"
    #     }
    #     response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTARbJEK", data=data)
    #     assert response.status_code == status.HTTP_200_OK
    #     assert list(self.savedTrack.album.albumArtists.all())[0].name == "Sum 41"
        

    # """
    # Updating the album artists name with a string with the highest length allowed.
    # """
    # def test_trackPutAlbumArtistsLongestName(self):
    #     data = {
    #         "albumName": "Chuck",
    #         "albumArtistsName": "a" * 100
    #     }
    #     response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTARbJEK", data=data)
    #     assert response.status_code == status.HTTP_200_OK
    #     assert list(self.savedTrack.album.albumArtists.all())[0].name == "a" * 100
        

    """
    The "albumName" field is null. The updated value must be None.
    """
    def test_trackPutAlbumArtistsNull(self):
        data = {
            "albumName": "Chuck",
            "albumArtistsName": None
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTADDKDK", data=data)
        assert response.status_code == status.HTTP_200_OK
        pprint.pp("albumartistd")
        pprint.pp(list(self.savedTrack.album.albumArtists.all()))
        assert len(list(self.savedTrack.album.albumArtists.all())) == 0


    # """
    # Trying to update the album artists name field without specifying the album field should fail 
    # with a 400 error code.
    # """
    # def test_trackPutAlbumArtistsAlbumMissing(self):

    #     data = {
    #         "albumArtistsName": "Muse",
    #     }
    #     response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTADDKDK", data=data)
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST


    # """
    # Trying to update the album artists name specifying a null album name field should fail with a 
    # 400 error code.
    # """
    # def test_trackPutAlbumArtistsAlbumNull(self):

    #     data = {
    #         "albumName": None,
    #         "albumArtistsName": "Muse",
    #     }
    #     response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTADDKDK", data=data)
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
