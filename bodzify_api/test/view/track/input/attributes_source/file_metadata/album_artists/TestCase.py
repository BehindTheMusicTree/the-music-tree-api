#!/usr/bin/env python

import logging
from bodzify_api import settings
from bodzify_api.test.view.track.input.attributes_source.file_metadata.FieldStrFromFileMetadataTestCase \
    import FieldStrNullableFromFileMetadataTestCase
from rest_framework import status


class TestCase(FieldStrNullableFromFileMetadataTestCase):
    file_extension: str

    def test_none_then_none(self):
        response = \
            self.post_lib_track_with_generic_sample_tag_album_koko_without_album_artists(extension=self.file_extension)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.lib_track_saved.album is not None
        assert self.lib_track_saved.album.album_artists.count() == 0

    def test_longest(self):
        response = self.post_lib_track_with_generic_sample_tags_max_length_of_a(
            extension=self.file_extension)  # type: ignore
        assert response.status_code == status.HTTP_201_CREATED

        expected_name = 'a' * settings.ARTIST_NAME_LEN_MAX
        assert self.lib_track_saved.album is not None
        assert self.lib_track_saved.album.album_artists.all().first().name == expected_name


class Mp3TestCase(TestCase):
    file_extension = 'mp3'


class FlacTestCase(TestCase):
    file_extension = 'flac'


class WavTestCase(TestCase):
    file_extension = 'wav'
