from typing import cast
from rest_framework import status

from bodzify_api import settings
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_album_and_album_artists_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_LONG_A_ID3V2_SMALL_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        assert self.saved_object.album.name == "a" * settings.ALBUM_NAME_LEN_MAX
        assert self.saved_object.album.album_artists.count() == 1
        assert cast(Artist, self.saved_object.album.album_artists.first()).name == 'a' * settings.ARTIST_NAME_LEN_MAX

    def test_album_but_no_album_artist_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.ALBUM_KOKO_ID3V2_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        assert self.saved_object.album.name == "koko"
        assert self.saved_object.album.album_artists.count() == 0

    def test_no_album_but_album_artist_then_no_extraction(self):
        response = self._post_lib_track(TestLibTrackFilename.ALBUM_ARTISTS_MUSE_ID3V2_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album == None
