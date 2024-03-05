#!/usr/bin/env python

import pytest
from rest_framework import status

from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


@pytest.mark.django_db
class TestCase(ApiViewTestCase):

    def test_mp3_then_none(self):
        response = self.post_lib_track_with_generic_sample_no_tags(extension="mp3")
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.rating == None

    def test_wav_then_none(self):
        response = self.post_lib_track_with_generic_sample_no_tags(extension="wav")
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.rating == None

    def test_flac_then_none(self):
        response = self.post_lib_track_with_generic_sample_no_tags(extension="flac")
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.rating == None
