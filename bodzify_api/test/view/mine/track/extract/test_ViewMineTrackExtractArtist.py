#!/usr/bin/env python
import os
from rest_framework import status
from bodzify_api.test.view.mine.track.MineTrackViewTestCase import (
    MineTrackExtractViewTestCase)
from bodzify_api.model.criteria.Criteria import CriteriaSpecialNames
import bodzify_api.settings as settings


class MineTrackExtractViewTestCaseExistingArtist(MineTrackExtractViewTestCase):


    """
    With existing artist.
    """
    def test_mineTrackExtractArtistExisting(self):
        trackUrl = ("https://cs9-15v4.vkuseraudio.net/s/v1/acmp/qCKkBk5i-Rl-QBdJM2m2lGbeRX6gB2ji" +
                    "zqo-ZXY7dSsA7VYaDDbb7nHloh42XVdi1gZ-U0BtWIa1I5qZJ3RspFGJbomdr4P-LwffbPvwWnZ" +
                    "_hyJ2dSP4WIET6pg2tz6yUtco3HKAodQaY85KeQocwpIiOzKLUb1hDAf5a7xQ9_NrLESvCw.mp3")
        data = {
            "url": trackUrl,
            "title": "Summer Moved On",
            "artistName": "a-ha",
            "releasedOn": 1290292
        }
        response = self._loginAndExtract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.artist.name == "a-ha"
        assert self.savedTrack.album == None
        assert self.savedTrack.genre.name == CriteriaSpecialNames.GENRE_GENRELESS
        assert self.savedTrack.rating == 0
        assert self.savedTrack.file.name == (
            self.testUserLibraryRelativePath + "a-ha_-_Summer_Moved_On.mp3")
        assert os.path.exists(settings.MEDIA_ROOT + self.savedTrack.file.name)
