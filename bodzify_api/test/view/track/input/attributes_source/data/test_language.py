from rest_framework import status

from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.utils.field.body_data.type.to_extend_from.NullableCharBodyDataTestCase import (
    NullableCharBodyDataTestCase
)


class LanguageTestCase(NullableCharBodyDataTestCase):
    post_field_key = PostFields.LANGUAGE

    def test_value_then_ok(self):
        value = 'fr'
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3, **{PostFields.LANGUAGE: value})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.language == value

    def test_empty_then_none(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3, **{PostFields.LANGUAGE: ""})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.language == None
