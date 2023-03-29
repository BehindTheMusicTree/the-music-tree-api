#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api import settings
from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.test.view.mine.track.MineTrackViewTestCase import (
    MineTrackExtractViewTestCase)


class MineTrackViewExtractAlbumArtistsTestCase(MineTrackExtractViewTestCase):        

    """
    Updating the album artists name with a string with the highest length allowed.
    """
    def test_longest(self):
        trackUrl = ("https://cs9-15v4.vkuseraudio.net/s/v1/acmp/qCKkBk5i-Rl-QBdJM2m2lGbeRX6gB2ji" +
                    "zqo-ZXY7dSsA7VYaDDbb7nHloh42XVdi1gZ-U0BtWIa1I5qZJ3RspFGJbomdr4P-LwffbPvwWnZ" +
                    "_hyJ2dSP4WIET6pg2tz6yUtco3HKAodQaY85KeQocwpIiOzKLUb1hDAf5a7xQ9_NrLESvCw.mp3")
        data = {
            "url": trackUrl,
            "albumName": "Chuck",
            "albumArtistsName": "a" * settings.ALBUM_ARTISTS_FIELD_MAX_CHAR
        }
        response = self._loginAndExtract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert list(self.savedTrack.album.albumArtists.all())[0].name == (
            "a" * settings.ALBUM_ARTISTS_FIELD_MAX_CHAR)
        

    """
    The "albumName" field is null. The updated value must be None.
    """
    def test_null(self):
        trackUrl = ("https://cs9-15v4.vkuseraudio.net/s/v1/acmp/qCKkBk5i-Rl-QBdJM2m2lGbeRX6gB2ji" +
                    "zqo-ZXY7dSsA7VYaDDbb7nHloh42XVdi1gZ-U0BtWIa1I5qZJ3RspFGJbomdr4P-LwffbPvwWnZ" +
                    "_hyJ2dSP4WIET6pg2tz6yUtco3HKAodQaY85KeQocwpIiOzKLUb1hDAf5a7xQ9_NrLESvCw.mp3")
        data = {
            "url": trackUrl,
            "albumName": "Chuck",
            "albumArtistsName": None
        }
        response = self._loginAndExtract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert len(list(self.savedTrack.album.albumArtists.all())) == 0


    """
    Trying to update the album artists name field without specifying the album field should fail 
    with a 400 error code.
    """
    def test_albumMissing(self):
        trackUrl = ("https://cs9-15v4.vkuseraudio.net/s/v1/acmp/qCKkBk5i-Rl-QBdJM2m2lGbeRX6gB2ji" +
                    "zqo-ZXY7dSsA7VYaDDbb7nHloh42XVdi1gZ-U0BtWIa1I5qZJ3RspFGJbomdr4P-LwffbPvwWnZ" +
                    "_hyJ2dSP4WIET6pg2tz6yUtco3HKAodQaY85KeQocwpIiOzKLUb1hDAf5a7xQ9_NrLESvCw.mp3")
        data = {
            "url": trackUrl,
            "albumArtistsName": "Muse",
        }
        response = self._loginAndExtract(data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


    """
    Trying to update the album artists name specifying a null album name field should fail with a 
    400 error code.
    """
    def test_albumNull(self):
        trackUrl = ("https://cs9-15v4.vkuseraudio.net/s/v1/acmp/qCKkBk5i-Rl-QBdJM2m2lGbeRX6gB2ji" +
                    "zqo-ZXY7dSsA7VYaDDbb7nHloh42XVdi1gZ-U0BtWIa1I5qZJ3RspFGJbomdr4P-LwffbPvwWnZ" +
                    "_hyJ2dSP4WIET6pg2tz6yUtco3HKAodQaY85KeQocwpIiOzKLUb1hDAf5a7xQ9_NrLESvCw.mp3")
        data = {
            "url": trackUrl,
            "albumName": None,
            "albumArtistsName": "Muse",
        }
        response = self._loginAndExtract(data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


    """
    The update specifies the same album name as the existing one but without a "albumArtistsName" 
    field. As the previous track's album had an album artist, the update should link the track to 
    a new album with the same name but with no album artist.
    """
    def test_albumArtistsNotSpecified(self):
        sumArtist = G(Artist, user=self.testUser, name="Sum 41")
        albumName = "Chuck"
        chuckAlbum = G(Album, user=self.testUser, name=albumName, albumArtists=[sumArtist])
        trackUrl = ("https://cs9-15v4.vkuseraudio.net/s/v1/acmp/qCKkBk5i-Rl-QBdJM2m2lGbeRX6gB2ji" +
                    "zqo-ZXY7dSsA7VYaDDbb7nHloh42XVdi1gZ-U0BtWIa1I5qZJ3RspFGJbomdr4P-LwffbPvwWnZ" +
                    "_hyJ2dSP4WIET6pg2tz6yUtco3HKAodQaY85KeQocwpIiOzKLUb1hDAf5a7xQ9_NrLESvCw.mp3")
        data = {
            "url": trackUrl,
            "albumName": albumName
        }
        response = self._loginAndExtract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.album_id != chuckAlbum.uuid
        assert len(list(self.savedTrack.album.albumArtists.all())) == 0
