#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.mine.track.MineTrackViewTestCase import (
        MineTrackExtractViewTestCase)


class MineTrackViewExtractTitleTestCase(MineTrackExtractViewTestCase):


    """
    Trying to extract a track without providing a title would set the filename as the title 
    (here "MartijnSchmit-VacsInTheMorning").
    """
    def test_missing(self):
        trackUrl = ("https://ia801408.us.archive.org/31/items/martijn-schmit-vacs-in-the-"
                + "morning/MartijnSchmit-VacsInTheMorning.mp3")
        data = {
            "url": trackUrl
        }
        response = self._loginAndExtract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.title == "MartijnSchmit-VacsInTheMorning"
        

    """
    Trying to extract a track without providing a title would set the filename as the title.
    Here the filename has a length greater than the maximum number of characters allowed in a 
    title (178 > 100). Thus it is replaced by a random string.
    """
    def test_missingAndFilenameTooLong(self):
        trackUrl = ("https://cs9-7v4.vkuseraudio.net/s/v1/acmp/i18p_zFWiH7jmzEvvkfhv21apWdJuIW5LJox"
        + "oSpJB9lqmTJK0HsSL7ZMerTX11oDXuFyCHXiqBZS5uKvikGDbs6Gcj1pinujYLx4JURjpPwxIIPE_KN414JidBi"
        + "kY2vr290mJGqYNS544KrzQ1v-dqVY2hRtEfeoqwlRhgJQ3KpZMhmV2A.mp3")
        data = {
            "url": trackUrl,
        }
        response = self._loginAndExtract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
