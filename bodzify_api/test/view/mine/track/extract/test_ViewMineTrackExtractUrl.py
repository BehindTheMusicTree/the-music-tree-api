#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.mine.track.MineTrackViewTestCase import (
        MineTrackExtractViewTestCase)


class MineTrackExtractViewTestUrl(MineTrackExtractViewTestCase):

    fixtures = ['initial_data', 'TestUserData']

    """
    Trying to extract a track from a wrong url should fail with a 400 (bad request).
    """
    def test_mineTrackExtrackUrlWrong(self):
        self._login(self.testUser)

        trackUrl = ("https://wrong-url_OIJOIEFHPOEIHFEPOFIHEOFIH.mp3")
        data = {
            "url": trackUrl,
            "title": "du rap",
            "artistName": "Jul",
            "releasedOn": 1290292
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
