#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api import settings


class FilenameTestCase(ApiViewTestCase):

    def test_providingTitleAndArtistNameInData(self):
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "title": "I'm Here",
            "artistName": "Roméo",
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.filename == "Roméo_-_Im_Here.wav"

    def test_providingOnlyTitle(self):
        trackUrl = (
            "https://cs9-7v4.vkuseraudio.net/s/v1/acmp/i18p_zFWiH7jmzEvvkfhv21apWdJuIW5LJox"
            + "oSpJB9lqmTJK0HsSL7ZMerTX11oDXuFyCHXiqBZS5uKvikGDbs6Gcj1pinujYLx4JURjpPwxIIPE"
            + "_KN414JidBikY2vr290mJGqYNS544KrzQ1v-dqVY2hRtEfeoqwlRhgJQ3KpZMhmV2A.mp3")
        title = "Hellö"
        data = {
            "url": trackUrl,
            "title": title,
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.filename == title + ".mp3"

    def test_withoutProvidingTitleNorArtistAndOriginalFilenameTooLong(self):
        trackUrl = (
            "https://cs9-7v4.vkuseraudio.net/s/v1/acmp/i18p_zFWiH7jmzEvvkfhv21apWdJuIW5LJox"
            + "oSpJB9lqmTJK0HsSL7ZMerTX11oDXuFyCHXiqBZS5uKvikGDbs6Gcj1pinujYLx4JURjpPwxIIPE"
            + "_KN414JidBikY2vr290mJGqYNS544KrzQ1v-dqVY2hRtEfeoqwlRhgJQ3KpZMhmV2A.mp3")
        data = {
            "url": trackUrl
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert len(self.savedTrack.filename) == \
            settings.TRACK_FILENAME_GENERATED_WITHOUT_EXTENSION_LEN
