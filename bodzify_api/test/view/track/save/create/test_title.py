#!/usr/bin/env python
from rest_framework import status
from bodzify_api import settings
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TrackViewExtractTitleTestCase(ApiViewTestCase):

    def test_missingThenSetFromFilenameAsItsNotTooLong(self):
        filename = "MartijnSchmit-VacsInTheMorning"
        trackUrl = ("https://ia801408.us.archive.org/31/items/martijn-schmit-vacs-in-the-"
                    + "morning/" + filename + ".mp3")
        data = {
            "url": trackUrl
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.title == filename

    def test_missingAndFilenameTooLongSoRandomStringWithAppPrefix(self):
        trackUrl = (
            "https://cs9-7v4.vkuseraudio.net/s/v1/acmp/i18p_zFWiH7jmzEvvkfhv21apWdJuIW5LJox"
            + "oSpJB9lqmTJK0HsSL7ZMerTX11oDXuFyCHXiqBZS5uKvikGDbs6Gcj1pinujYLx4JURjpPwxIIPE"
            + "_KN414JidBikY2vr290mJGqYNS544KrzQ1v-dqVY2hRtEfeoqwlRhgJQ3KpZMhmV2A.mp3")
        data = {
            "url": trackUrl,
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.title.startswith(settings.TRACK_GENERATED_TITLE_PREFIXE)
        assert len(self.savedTrack.title) == settings.TRACK_GENERATED_TITLE_LEN
