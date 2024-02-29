#!/usr/bin/env python

import logging
from bodzify_api import settings
from bodzify_api.test.view.track.input.source.file_metadata.FieldStrFromFileMetadataTestCase \
    import FieldStrFromFileMetadataTestCase
from rest_framework import status

logger = logging.getLogger('bodzify_api')


class TestCase(FieldStrFromFileMetadataTestCase):
    file_extension = None

    def test_none_then_none(self):
        response = self.post_lib_track_with_generic_sample_tag_album_without_album_artists(
            generic_sample_extension=self.file_extension)  # type: ignore
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.album.album_artists.count() == 0  # type: ignore

    def test_longest(self):
        response = self.post_lib_track_with_generic_sample_tags_max_length_of_a(
            generic_sample_extension=self.file_extension)  # type: ignore
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore

        expected_name = 'a' * settings.ARTIST_NAME_LENGTH_MAX
        assert self.saved_lib_track.album.album_artists.all().first().name == expected_name  # type: ignore


class Mp3TestCase(TestCase):
    file_extension = 'mp3'


class FlacTestCase(TestCase):
    file_extension = 'flac'


class WavTestCase(TestCase):
    file_extension = 'wav'
