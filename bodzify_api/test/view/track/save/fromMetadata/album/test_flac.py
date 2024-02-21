#!/usr/bin/env python
import pytest
from rest_framework import status

from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


@pytest.mark.django_db
class FlacTestCase(ApiViewTestCase):

    def test_none_then_none(self):
        response = self.post_sample_track(
            sample_filename="none_then_none.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.album == None

    def test_longest(self):
        response = self.post_sample_track(
            sample_filename="100_char_album_name.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.album.name == "q{9SVjJ5{gE&_!7iu[?ti:QT6D/j" + \
            "=,zYyJfmj9pRP$U-WK$0rvxD5{B66{Kbp_P{0pV0bR.xDnVA48dLTgfFu96u&" + \
            "-X#SYQe=WqA"
