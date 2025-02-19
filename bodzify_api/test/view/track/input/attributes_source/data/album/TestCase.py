from rest_framework import status

from bodzify_api.serializer.schema.model.lib_track.input.post import Fields as PostFields
from bodzify_api.test.field.body_data.type.NullableBodyDataTestCase import NullableBodyDataTestCase
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(LibTrackTestCase, NullableBodyDataTestCase):
    post_field_key = PostFields.ALBUM_NAME

    def test_value_then_ok(self):
        value = 'fofof'
        response = self._post_lib_track_with_generic_sample_no_tags(**{PostFields.ALBUM_NAME: value})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        assert self.saved_object.album.name == value

    def test_empty_then_none(self):
        response = self._post_lib_track_with_generic_sample_1_star(**{PostFields.ALBUM_NAME: ""})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album == None

    def test_multiple_values_then_error(self):
        # As
