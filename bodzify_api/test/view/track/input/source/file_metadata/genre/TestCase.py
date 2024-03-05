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
            generic_sample_extension=self.file_extension)  # type: ignore
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.genre == None

    def test_longest(self):
        response = self.post_lib_track_with_generic_sample_tags_max_length_of_a(
            generic_sample_extension=self.file_extension)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.genre.name == 'a' * settings.CRITERIA_NAME_LENGTH_MAX  # type: ignore


class Mp3TestCase(TestCase):
    file_extension = 'mp3'


class FlacTestCase(TestCase):
    file_extension = 'flac'


class WavTestCase(TestCase):
    file_extension = 'wav'
