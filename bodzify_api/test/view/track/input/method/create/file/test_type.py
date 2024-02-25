#!/usr/bin/env python

from rest_framework import status

from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TypeTestCase(ApiViewTestCase):

    def test_wav(self):
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav"
        }
        response = self.extract(json_data=data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_mp3(self):
        track_url = (
            "https://cs9-7v4.vkuseraudio.net/s/v1/acmp/i18p_zFWiH7jmzEvvkfhv21apWdJuIW5LJox"
            + "oSpJB9lqmTJK0HsSL7ZMerTX11oDXuFyCHXiqBZS5uKvikGDbs6Gcj1pinujYLx4JURjpPwxIIPE"
            + "_KN414JidBikY2vr290mJGqYNS544KrzQ1v-dqVY2hRtEfeoqwlRhgJQ3KpZMhmV2A.mp3")
        data = {
            "url": track_url,
        }
        response = self.extract(json_data=data)
        assert response.status_code == status.HTTP_201_CREATED
