#!/usr/bin/env python

import pytest
from rest_framework import status

from bodzify_api.test.view.track.input.source.file_metadata.FieldFromFileMetadataTestCase import \
    FieldFromFileMetadataTestCase


@pytest.mark.django_db
class TestCase(FieldFromFileMetadataTestCase):

    def test_none_then_none(self):
        response = self.post_lib_track_with_generic_sample_no_tags(generic_sample_extension="wav")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.language == None

    def test_longest(self):
        response = self.post_lib_track_with_specific_sample(specific_sample_filename="100_char language.wav")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.language == "4bTyH6zRq7Psk7Y9Pydmb4gTYs9VCVvehPANcaZHbviunfxtl5Kwj" + \
            "gJQdUyvX9WKnsv0KAtwAiWmi739Fqt2KsGZi7F3Fn9AXPI3"
