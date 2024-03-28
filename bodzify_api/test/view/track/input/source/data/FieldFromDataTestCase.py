#!/usr/bin/env python

from requests import post
from bodzify_api.serializer.track.input.schema.endpoint.LibTrackPostSerializer import FIELDS as POST_FIELDS
from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class FieldFromDataTestCase(TrackTestCase):
    post_field_key = None

    def setUp(self, methods_names_to_implement: list[str] | None = None):
        class_methods_names_to_implement = ['test_value_then_ok']
        if methods_names_to_implement:
            class_methods_names_to_implement += methods_names_to_implement
        return super().setUp(class_methods_names_to_implement)


class NullableFieldFromDataTestCase(FieldFromDataTestCase):

    def setUp(self, methods_names_to_implement: list[str] | None = None):
        class_methods_names_to_implement = ['test_empty_then_none']
        if methods_names_to_implement:
            class_methods_names_to_implement += methods_names_to_implement
        return super().setUp(class_methods_names_to_implement)


class NonNullableFieldFromDataTestCase(FieldFromDataTestCase):

    def test_empty_then_error(self):
        data = {self.post_field_key: ""}
        response = self.post_lib_track_with_generic_sample_no_tags(extension='mp3', data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore


class TitleTestCase(NonNullableFieldFromDataTestCase):

    def test_value_then_ok(self):
        value = 'fr'
        data = {POST_FIELDS.TITLE: value}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.title == value
