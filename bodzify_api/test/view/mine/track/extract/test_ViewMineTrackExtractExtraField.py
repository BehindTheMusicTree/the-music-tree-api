#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.mine.track.MineTrackViewTestCase import (
        MineTrackExtractViewTestCase)


class MineTrackExtractViewTestCaseExtraField(MineTrackExtractViewTestCase):

    """
        Trying to extract a track with a field not handled should fail with a 400 (bad request).
    """
    def test_mineTrackExtractExtraField(self):
        self._login(self.testUser)
        trackUrl = ("https://cs9-15v4.vkuseraudio.net/s/v1/acmp/qCKkBk5i-Rl-QBdJM2m2lGbeRX6gB2ji" +
                    "zqo-ZXY7dSsA7VYaDDbb7nHloh42XVdi1gZ-U0BtWIa1I5qZJ3RspFGJbomdr4P-LwffbPvwWnZ" +
                    "_hyJ2dSP4WIET6pg2tz6yUtco3HKAodQaY85KeQocwpIiOzKLUb1hDAf5a7xQ9_NrLESvCw.mp3")
        data = {
            "url": trackUrl,
            "title": "Summer Moved On",
            "fieldNotHandled": "a-ha"
        }

        response = self._loginAndExtract(data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
