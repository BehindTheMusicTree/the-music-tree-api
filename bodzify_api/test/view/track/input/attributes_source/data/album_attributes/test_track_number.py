from rest_framework import status

from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_value_then_ok(self):
        value = 1
        data = {PostFields.ALBUM_NAME: 'albumito',
                PostFields.ALBUM_ARTISTS_NAMES_ARRAY: [],
                PostFields.TRACK_NUMBER: value}
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_number == value

    def test_empty_then_none(self):
        data = {PostFields.ALBUM_NAME: "albumito",
                PostFields.ALBUM_ARTISTS_NAMES_ARRAY: [],
                PostFields.TRACK_NUMBER: None}
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_number == None

    def test_not_provided_then_none(self):
        data = {PostFields.ALBUM_NAME: "albumito",
                PostFields.ALBUM_ARTISTS_NAMES_ARRAY: []}
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_number == None
