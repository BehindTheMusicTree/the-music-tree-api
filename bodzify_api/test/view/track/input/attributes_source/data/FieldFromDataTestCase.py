from typing import Optional
from rest_framework import status

from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class FieldFromDataTestCase(LibTrackTestCase):
    post_field_key: Optional[str] = None

    def setUp(self, methods_names_to_implement: list[str] | None = None):
        class_methods_names_to_implement = ['test_value_then_ok']
        if methods_names_to_implement:
            class_methods_names_to_implement += methods_names_to_implement
        return super().setUp(class_methods_names_to_implement)


class FieldStrFromDataTestCase(FieldFromDataTestCase):

    def test_multiple_values_then_error(self):
        if not self.post_field_key:
            raise NotImplementedError("post_field_key is not set")
        data = {self.post_field_key: ["value", "value2"]}
        response = self._post_lib_track_with_generic_sample_no_tags(kwargs=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class FieldIntFromDataTestCase(FieldFromDataTestCase):

    def test_field_twice_then_error(self):
        if not self.post_field_key:
            raise NotImplementedError("post_field_key is not set")
        response = self._post_lib_track_with_generic_sample_no_tags(kwargs={self.post_field_key: [1, 2]})
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class NullableStrFieldFromDataTestCase(FieldStrFromDataTestCase):

    def setUp(self, methods_names_to_implement: list[str] | None = None):
        class_methods_names_to_implement = ['test_empty_then_none']
        if methods_names_to_implement:
            class_methods_names_to_implement += methods_names_to_implement
        return super().setUp(class_methods_names_to_implement)


class NullableUuidFieldFromDataTestCase(NullableStrFieldFromDataTestCase):

    def setUp(self, methods_names_to_implement: list[str] | None = None):
        class_methods_names_to_implement = ['test_non_existing_uuid_then_error']
        if methods_names_to_implement:
            class_methods_names_to_implement += methods_names_to_implement
        return super().setUp(class_methods_names_to_implement)


class NonNullableStrFieldFromDataTestCase(FieldStrFromDataTestCase):

    def test_empty_then_error(self):
        data = {self.post_field_key: ""}
        response = self._post_lib_track_with_generic_sample_no_tags(extension='mp3', data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
