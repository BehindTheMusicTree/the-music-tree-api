

from rest_framework import status

from bodzify_api.model.artist.Artist import Artist
from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.utils.lib_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_value_then_ok(self):
        value = 'outkast'
        data = {
            PostFields.ALBUM_NAME: 'albumito',
            PostFields.ALBUM_ARTISTS_NAMES_MULTIPART: value
        }
        response = self._post_lib_track(LibTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        artist: Artist | None = self.saved_object.album.album_artists.first()
        assert artist
        assert artist.name == value

    def test_empty_then_none(self):
        data = {PostFields.ALBUM_NAME: "albumito", PostFields.ALBUM_ARTISTS_NAMES_MULTIPART: []}
        response = self._post_lib_track(LibTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        assert self.saved_object.album.album_artists.count() == 0
