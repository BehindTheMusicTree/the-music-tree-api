#!/usr/bin/env python

from rest_framework import status

from bodzify_api.serializer.track.input.endpoint.post import \
    Fields as PostFields
from bodzify_api.test.view.track.input.attributes_source.data.FieldFromDataTestCase import \
    NullableStrFieldFromDataTestCase


class AlbumTestCase(NullableStrFieldFromDataTestCase):
    post_field_key = PostFields.ALBUM_NAME

    def test_value_then_ok(self):
        value = 'fofof'
        data = {PostFields.ALBUM_NAME: value}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.lib_track_saved.album.name == value  # type: ignore

    def test_empty_then_none(self):
        data = {PostFields.ALBUM_NAME: ""}
        response = self.post_lib_track_with_generic_sample_1_star(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.lib_track_saved.album == None
