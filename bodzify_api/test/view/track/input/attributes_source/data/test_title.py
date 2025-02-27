from rest_framework import status

from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.utils.field.body_data.type.NotNullableCharBodyDataTestCase import NotNullableCharBodyDataTestCase
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename


class TitleTestCase(NotNullableCharBodyDataTestCase):
    post_field_key = PostFields.TITLE

    def test_value_then_ok(self):
        value = 'fr'
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3, **{PostFields.TITLE: value})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title == value
