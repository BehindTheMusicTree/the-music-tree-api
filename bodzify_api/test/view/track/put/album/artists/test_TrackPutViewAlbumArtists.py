#!/usr/bin/env python
import pprint
from rest_framework import status
from bodzify_api.model.Album import Album
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


class TrackPutViewTestCaseAlbumArtists(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutDataAlbumArtists']
        

    """
    Updating the album artists name with a string with the highest length allowed.
    """
    def test_trackPutAlbumArtistsLongestName(self):
        data = {
            "albumName": "Chuck",
            "albumArtistsName": "a" * 100
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTARbJEK", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert list(self.savedTrack.album.albumArtists.all())[0].name == "a" * 100
        

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
        assert len(list(self.savedTrack.album.albumArtists.all())) == 0


    """
    Trying to update the album artists name field without specifying the album field should fail 
    with a 400 error code.
    """
    def test_trackPutAlbumArtistsAlbumMissing(self):

        data = {
            "albumArtistsName": "Muse",
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTADDKDK", data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


    """
    Trying to update the album artists name specifying a null album name field should fail with a 
    400 error code.
    """
    def test_trackPutAlbumArtistsAlbumNull(self):

        data = {
            "albumName": None,
            "albumArtistsName": "Muse",
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTADDKDK", data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


    """
    The update specifies the same album name as the existing one but without a "albumArtistsName" 
    field. As the previous track's album had an album artist, the update should link the track to 
    a new album with the same name but with no album artist.
    """
    def test_trackPutAlbumArtistsMissing(self):
        data = {
            "albumName": "Chuck"
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTARbJEK", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.album_id != "Lsji85mqisjdjf88DDLSK"
        assert len(list(self.savedTrack.album.albumArtists.all())) == 0
