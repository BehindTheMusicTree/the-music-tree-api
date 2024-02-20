#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api import settings


class FilenameTestCase(ApiViewTestCase):

    def test_providingTitleAndartist_nameInData(self):
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "title": "I'm Here",
            "artist_name": "Roméo",
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.filename == "Roméo_-_Im_Here.wav"

    def test_providing_only_title_in_data_then_filename_with_title(self):
        track_url = (
            "https://cs9-7v4.vkuseraudio.net/s/v1/acmp/i18p_zFWiH7jmzEvvkfhv21apWdJuIW5LJox"
            + "oSpJB9lqmTJK0HsSL7ZMerTX11oDXuFyCHXiqBZS5uKvikGDbs6Gcj1pinujYLx4JURjpPwxIIPE"
            + "_KN414JidBikY2vr290mJGqYNS544KrzQ1v-dqVY2hRtEfeoqwlRhgJQ3KpZMhmV2A.mp3")
        title = "Hellö"
        data = {
            "url": track_url,
            "title": title,
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.filename == title + ".mp3"

    def test_not_providing_title_nor_artist_and_original_filename_too_long_then_generate_filename(self):
        track_url = (
            "https://cs9-7v4.vkuseraudio.net/s/v1/acmp/i18p_zFWiH7jmzEvvkfhv21apWdJuIW5LJox"
            + "oSpJB9lqmTJK0HsSL7ZMerTX11oDXuFyCHXiqBZS5uKvikGDbs6Gcj1pinujYLx4JURjpPwxIIPE"
            + "_KN414JidBikY2vr290mJGqYNS544KrzQ1v-dqVY2hRtEfeoqwlRhgJQ3KpZMhmV2A.mp3")
        data = {
            "url": track_url
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert len(self.saved_track.filename) == \
            settings.TRACK_FILENAME_GENERATED_WITHOUT_EXTENSION_LEN
