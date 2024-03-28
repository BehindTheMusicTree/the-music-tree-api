#!/usr/bin/env python

from rest_framework import status
from bodzify_api import settings
from bodzify_api.serializer.track.input.schema.endpoint.LibTrackExtractSerializer import FIELDS as EXTRACT_FIELDS
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class FilenameTestCase(TrackTestCase):

    def test_title_and_artist_name_in_data_then_filename_with_artist_and_title(self):
        data_dict = {
            EXTRACT_FIELDS.TITLE: "ImHere",
            EXTRACT_FIELDS.ARTIST_NAME: "Roméo",
        }
        response = self.extract_default_mine_track(data_dict=data_dict)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.filename == f"Roméo_-_ImHere.{TrackTestCase.SAMPLE_MINE_TRACK_DEFAULT_EXTENSION}"

    def test_title_and_artist_with_spaces_then_filename_without_spaces(self):
        data_dict = {
            EXTRACT_FIELDS.TITLE: "Im Here",
            EXTRACT_FIELDS.ARTIST_NAME: "Rom éo",
        }
        response = self.extract_default_mine_track(data_dict=data_dict)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.filename == f"Rom_éo_-_Im_Here.{TrackTestCase.SAMPLE_MINE_TRACK_DEFAULT_EXTENSION}"

    def test_title_and_artist_with_special_characyers_then_filename_without_them(self):
        data_dict = {
            EXTRACT_FIELDS.TITLE: "I'm Here",
            EXTRACT_FIELDS.ARTIST_NAME: "Rom#éo",
        }
        response = self.extract_default_mine_track(data_dict=data_dict)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.filename == f"Roméo_-_Im_Here.{TrackTestCase.SAMPLE_MINE_TRACK_DEFAULT_EXTENSION}"

    def test_only_title_in_data_then_filename_with_title(self):
        title = "Hellö"
        data_dict = {
            EXTRACT_FIELDS.TITLE: title
        }
        response = self.extract_default_mine_track(data_dict=data_dict)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.filename == f"{title}.{TrackTestCase.SAMPLE_MINE_TRACK_DEFAULT_EXTENSION}"

    def test_not_providing_title_nor_artist_and_original_filename_too_long_then_generate_filename(self):
        track_url = (
            "https://cs9-7v4.vkuseraudio.net/s/v1/acmp/i18p_zFWiH7jmzEvvkfhv21apWdJuIW5LJox"
            + "oSpJB9lqmTJK0HsSL7ZMerTX11oDXuFyCHXiqBZS5uKvikGDbs6Gcj1pinujYLx4JURjpPwxIIPE"
            + "_KN414JidBikY2vr290mJGqYNS544KrzQ1v-dqVY2hRtEfeoqwlRhgJQ3KpZMhmV2A.mp3")
        data_dict = {
            EXTRACT_FIELDS.URL: track_url
        }
        response = self.extract(data_dict=data_dict)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert len(self.saved_lib_track.filename) == settings.LIB_TRACK_FILENAME_GENERATED_WITHOUT_EXTENSION_LENGTH
