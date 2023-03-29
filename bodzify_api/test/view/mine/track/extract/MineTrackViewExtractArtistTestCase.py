#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.model.Artist import Artist
from bodzify_api.test.view.mine.track.MineTrackViewTestCase import (
    MineTrackExtractViewTestCase)


class MineTrackViewExtractArtistTestCase(MineTrackExtractViewTestCase):

    """
    With existing artist.
    """
    def test_existing(self):
        artistName = "a-ha"
        ahaArtist = G(Artist, user=self.testUser, name=artistName)
        trackUrl = ("https://cs9-15v4.vkuseraudio.net/s/v1/acmp/qCKkBk5i-Rl-QBdJM2m2lGbeRX6gB2ji" +
                    "zqo-ZXY7dSsA7VYaDDbb7nHloh42XVdi1gZ-U0BtWIa1I5qZJ3RspFGJbomdr4P-LwffbPvwWnZ" +
                    "_hyJ2dSP4WIET6pg2tz6yUtco3HKAodQaY85KeQocwpIiOzKLUb1hDAf5a7xQ9_NrLESvCw.mp3")
        data = {
            "url": trackUrl,
            "artistName": artistName,
        }
        response = self._loginAndExtract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.artist.name == artistName
        
        
    """
    With non existing artist.
    """
    def test_notExisting(self):
        artistName = "hoho"
        trackUrl = ("https://cs9-15v4.vkuseraudio.net/s/v1/acmp/qCKkBk5i-Rl-QBdJM2m2lGbeRX6gB2ji" +
                    "zqo-ZXY7dSsA7VYaDDbb7nHloh42XVdi1gZ-U0BtWIa1I5qZJ3RspFGJbomdr4P-LwffbPvwWnZ" +
                    "_hyJ2dSP4WIET6pg2tz6yUtco3HKAodQaY85KeQocwpIiOzKLUb1hDAf5a7xQ9_NrLESvCw.mp3")
        data = {
            "url": trackUrl,
            "artistName": artistName,
        }
        response = self._loginAndExtract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.artist.name == artistName
