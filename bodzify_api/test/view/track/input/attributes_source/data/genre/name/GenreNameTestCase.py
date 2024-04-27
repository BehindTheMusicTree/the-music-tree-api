#!/usr/bin/env python

import pytest
from bodzify_api.test import conftest
from bodzify_api.serializer.track.input.endpoint.LibTrackPostSerializer import FIELDS as POST_FIELDS
from rest_framework import status

from bodzify_api.test.view.track.input.attributes_source.data.FieldFromDataTestCase import NullableStrFieldFromDataTestCase


class GenreNameTestCase(NullableStrFieldFromDataTestCase):
    post_field_key = POST_FIELDS.GENRE_NAME

    def test_value_then_ok(self):
        value = 'rovk'
        data = {POST_FIELDS.GENRE_NAME: value}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.genre.name == value  # type: ignore

    def test_empty_then_none(self):
        data = {POST_FIELDS.GENRE_NAME: ""}
        response = self.post_lib_track_with_generic_sample_1_star(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.genre == None
