#!/usr/bin/env python

import logging
from bodzify_api import settings
from bodzify_api.test.view.track.input.source.file_metadata.FieldStrFromFileMetadataTestCase \
    import FieldStrNullableFromFileMetadataTestCase
from rest_framework import status

logger = logging.getLogger('bodzify_api')


class TestCase(FieldStrNullableFromFileMetadataTestCase):
    file_extension = None

    def test_none_then_none(self):
        response = self.post_lib_track_with_generic_sample_no_tags(
            extension=self.file_extension)  # type: ignore
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.language == None

    def test_longest(self):
        response = self.post_lib_track_with_generic_sample_tags_max_length_of_a(
            extension=self.file_extension)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.language == 'a' * settings.LIB_TRACK_LANGUAGE_LENGTH_MAX


class Mp3TestCase(TestCase):
    file_extension = 'mp3'


class FlacTestCase(TestCase):
    file_extension = 'flac'


class WavTestCase(TestCase):
    file_extension = 'wav'
