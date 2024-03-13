#!/usr/bin/env python

from rest_framework import status
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_ok_when_max_length(self):
        sample_100_char_long_char_name = ("3NyKu2inI7MA3DIRa78qLuowTOppybbfKx27gzOV7aiHJNcDTIDxSJJMNNY" +
                                          "s5B2xZk7Ka11zddHC6qlc4zjGYjboNkvbmLTd.mp3")
        response = self.post_lib_track_with_specific_sample(
            specific_sample_filename=sample_100_char_long_char_name, data_dict={})
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore

    def test_error_when_too_long(self):
        sample_101_char_long_char_name = ("3NyKu2inI7MA3DIRa78qLuowTOppybbfKx27gzOV7aiHJNcDTIDxSJJMNNY" +
                                          "s5B2xZk7Ka11zddHC6qlc4zjGYjboNkvbmLTdv.mp3")
        response = self.post_lib_track_with_specific_sample(
            specific_sample_filename=sample_101_char_long_char_name, data_dict={})
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore
