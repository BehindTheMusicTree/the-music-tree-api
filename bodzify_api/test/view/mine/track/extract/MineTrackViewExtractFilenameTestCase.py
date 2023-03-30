#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.mine.track.MineTrackViewTestCase import (
        MineTrackExtractViewTestCase)


class MineTrackViewExtractFilenameTestCase(MineTrackExtractViewTestCase):

    """
    When extracting a mp3 track proviging a title "I'm Here" and an artist "Roméo", the resulting 
    filename should be "Roméo_-_Im_Here.mp3".
    """
    def test_withTitleAndArtistNameInData(self):
        trackUrl = ("https://cs9-7v4.vkuseraudio.net/s/v1/acmp/i18p_zFWiH7jmzEvvkfhv21apWdJuIW5LJox"
        + "oSpJB9lqmTJK0HsSL7ZMerTX11oDXuFyCHXiqBZS5uKvikGDbs6Gcj1pinujYLx4JURjpPwxIIPE_KN414JidBi"
        + "kY2vr290mJGqYNS544KrzQ1v-dqVY2hRtEfeoqwlRhgJQ3KpZMhmV2A.mp3")
        data = {
            "url": trackUrl,
            "title": "I'm Here",
            "artistName": "Roméo",
        }
        response = self._loginAndExtract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.filename == "Roméo_-_Im_Here.mp3"


    """
    When extracting a mp3 track proviging only a title ("Hellö") and no artist, the resulting 
    filename should be "Hellö.mp3".
    """
    def test_withOnlyTitle(self):
        trackUrl = ("https://cs9-7v4.vkuseraudio.net/s/v1/acmp/i18p_zFWiH7jmzEvvkfhv21apWdJuIW5LJox"
        + "oSpJB9lqmTJK0HsSL7ZMerTX11oDXuFyCHXiqBZS5uKvikGDbs6Gcj1pinujYLx4JURjpPwxIIPE_KN414JidBi"
        + "kY2vr290mJGqYNS544KrzQ1v-dqVY2hRtEfeoqwlRhgJQ3KpZMhmV2A.mp3")
        data = {
            "url": trackUrl,
            "title": "Hellö",
        }
        response = self._loginAndExtract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.filename == "Hellö.mp3"