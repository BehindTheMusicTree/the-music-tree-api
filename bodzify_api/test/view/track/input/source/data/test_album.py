#!/usr/bin/env python

from bodzify_api.serializer.track.input.schema.endpoint.LibTrackPostSerializer import FIELDS as POST_FIELDS
from rest_framework import status

from bodzify_api.test.view.track.input.source.data.FieldFromDataTestCase import NullableFieldFromDataTestCase


class TestCase(NullableFieldFromDataTestCase):

    def test_value_then_ok(self):
        value = 'fofof'
        data = {POST_FIELDS.ALBUM_NAME: value}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.album.name == value  # type: ignore

    def test_empty_then_none(self):
        data = {POST_FIELDS.ALBUM_NAME: ""}
        response = self.post_lib_track_with_generic_sample_1_star(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.album == None
