#!/usr/bin/env python

from math import e
from urllib import response
import pytest
from rest_framework import status

from bodzify_api.test.view.track.input.source.file_metadata.AttributeFromFileMetadataTestCase import \
    AttributeFromFileMetadataTestCase


@pytest.mark.django_db
class TestCase(AttributeFromFileMetadataTestCase):

    def test_none_then_none(self):
        response = self.post_lib_track_with_generic_sample_no_tags(generic_sample_extension="flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.album == None

    def test_longest(self):
        response = self.post_lib_track_with_generic_sample_tags_max_length_of_a(generic_sample_extension="flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.album.name == "q{9SVjJ5{gE&_!7iu[?ti:QT6D/j" + \
            "=,zYyJfmj9pRP$U-WK$0rvxD5{B66{Kbp_P{0pV0bR.xDnVA48dLTgfFu96u&" + \
            "-X#SYQe=WqA"
