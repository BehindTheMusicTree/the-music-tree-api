#!/usr/bin/env python

from rest_framework import status

from bodzify_api import settings
from bodzify_api.serializer.schema.track.input.endpoint.put import Fields as PutFields
from bodzify_api.test.view.track.input.save.FieldStrNullableTestCase import FieldStrNullableTestCase


class TestCase(FieldStrNullableTestCase):

    def test_longest_then_ok(self):
        language = "a" * settings.LIB_TRACK_LANGUAGE_LEN_MAX
        data = {PutFields.LANGUAGE: language}
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.language == language

    def test_too_long_then_error(self):
        language = "a" * (settings.LIB_TRACK_LANGUAGE_LEN_MAX + 1)
        data = {PutFields.LANGUAGE: language}
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_empty_then_none(self):
        data = {PutFields.LANGUAGE: ""}
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.language == None
