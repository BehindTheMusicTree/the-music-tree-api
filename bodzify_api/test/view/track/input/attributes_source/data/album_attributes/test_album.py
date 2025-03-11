from rest_framework import status

from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.utils.lib_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_value_then_ok(self):
        value = 'fofof'
        data = {PostFields.ALBUM_NAME: value, PostFields.ALBUM_ARTISTS_NAMES_ARRAY: []}
        response = self._post_lib_track(LibTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        assert self.saved_object.album.name == value

    def test_empty_then_none(self):
        response = self._post_lib_track(LibTrackTestFilename.METADATA_NONE_MP3, **{PostFields.ALBUM_NAME: ""})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album == None
