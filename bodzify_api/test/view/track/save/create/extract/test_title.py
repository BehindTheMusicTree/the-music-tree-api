#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api import settings


class TestCase(ApiViewTestCase):

    def test_notProvidingTitleNorArtistAndOriginalFilenameTooLongThenGenerateWithAppPrefixe(self):
        trackUrl = (
            "https://cs9-7v4.vkuseraudio.net/s/v1/acmp/i18p_zFWiH7jmzEvvkfhv21apWdJuIW5LJox"
            + "oSpJB9lqmTJK0HsSL7ZMerTX11oDXuFyCHXiqBZS5uKvikGDbs6Gcj1pinujYLx4JURjpPwxIIPE"
            + "_KN414JidBikY2vr290mJGqYNS544KrzQ1v-dqVY2hRtEfeoqwlRhgJQ3KpZMhmV2A.mp3")
        data = {
            "url": trackUrl
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.title.startswith(settings.TRACK_GENERATED_TITLE_PREFIXE)
