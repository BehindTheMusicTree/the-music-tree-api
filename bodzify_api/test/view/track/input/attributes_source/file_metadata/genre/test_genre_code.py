import pytest

from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_genre_code_from_riff_id3v2_then_genre_name(self):
        response = self._post_lib_track(
