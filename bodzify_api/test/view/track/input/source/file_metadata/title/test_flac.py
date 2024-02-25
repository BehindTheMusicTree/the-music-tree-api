#!/usr/bin/env python
from urllib import response
import pytest
from rest_framework import status
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


@pytest.mark.django_db
class FlacTestCase(ApiViewTestCase):

    def test_none_then_filename(self):
        response = self.post_lib_track_with_generic_sample_no_tags(generic_sample_extension="flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.title == filename

    def test_longest(self):
        response = self.post_lib_track_with_generic_sample_tags_max_length_of_a(generic_sample_extension="flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.title == "4bTyH6zRq7Psk7Y9Pydmb4gTYs9VCVvehPANcaZHbviunfxtl5Kwj" + \
            "gJQdUyvX9WKnsv0KAtwAiWmi739Fqt2KsGZi7F3Fn9AXPI3"
