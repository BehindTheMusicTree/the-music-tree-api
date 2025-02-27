from rest_framework import status

from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.utils.field.body_data.type.NullableCharBodyDataTestCase import NullableCharBodyDataTestCase
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(NullableCharBodyDataTestCase, LibTrackTestCase):
    post_field_key = PostFields.GENRE_NAME

    def test_value_then_ok(self):
        value = 'rovk'
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3, **{PostFields.GENRE_NAME: value})
        assert response.status_code == status.HTTP_201_CREATED
        genre = self.saved_object.genre
        assert genre
        assert genre.name == value

    def test_empty_then_none(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3, **{PostFields.GENRE_NAME: ""})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre == None
