#!/usr/bin/env python

from rest_framework import status

from bodzify_api.serializer.schema.track.input.endpoint.post import Fields as PostFields
from bodzify_api.test.view.track.input.attributes_source.data.FieldFromDataTestCase import \
    NullableStrFieldFromDataTestCase


class AlbumTestCase(NullableStrFieldFromDataTestCase):
    post_field_key = PostFields.ALBUM_NAME

    def test_value_then_ok(self):
        value = 'fofof'
        data = {PostFields.ALBUM_NAME: value}
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.album
        assert self.saved_lib_track.album.name == value

    def test_empty_then_none(self):
        data = {PostFields.ALBUM_NAME: ""}
        response = self._post_lib_track_with_generic_sample_1_star(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.album == None
