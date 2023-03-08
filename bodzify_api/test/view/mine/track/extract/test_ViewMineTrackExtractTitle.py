#!/usr/bin/env python
from rest_framework import status
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.mine.track.MineTrackViewTestCase import (
        MineTrackExtractViewTestCase)


class MineTrackExtractViewTestTitle(MineTrackExtractViewTestCase):

    fixtures = ['initial_data', 'TestUserData']

    """
    Trying to extract a track without providing a title would set the filename as the title.
    If the filename is too long (more than 100 characters), it is replaced by a random string
    of 20 characters.
    """
    def test_mineTrackExtractTitleMissing(self):
        self._login(self.testUser)

        trackUrl = ("https://cs9-7v4.vkuseraudio.net/s/v1/acmp/i18p_zFWiH7jmzEvvkfhv21apWdJuIW5LJox"
        + "oSpJB9lqmTJK0HsSL7ZMerTX11oDXuFyCHXiqBZS5uKvikGDbs6Gcj1pinujYLx4JURjpPwxIIPE_KN414JidBi"
        + "kY2vr290mJGqYNS544KrzQ1v-dqVY2hRtEfeoqwlRhgJQ3KpZMhmV2A.mp3")
        data = {
            "url": trackUrl,
            "artistName": "Jul",
            "releasedOn": 1290292
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_200_OK


    """
    Trying to extract a track without providing a title would set the filename as the title.
    If the filename is too long (more than 100 characters), it is replaced by a random string
    of 20 characters. Here "MartijnSchmit-VacsInTheMorning".
    """
    def test_mineTrackExtractTitleMissing(self):
        self._login(self.testUser)

        trackUrl = ("https://ia801408.us.archive.org/31/items/martijn-schmit-vacs-in-the-"
                + "morning/MartijnSchmit-VacsInTheMorning.mp3")
        data = {
            "url": trackUrl
        }
        self.extract(data=data)
        assert LibraryTrack.objects.filter(
                user=self.testUser, title="MartijnSchmit-VacsInTheMorning").exists()
