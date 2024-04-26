#!/usr/bin/env python

from bodzify_api.serializer.track.input.endpoint.LibTrackPostSerializer import FIELDS as POST_FIELDS
from rest_framework import status
from bodzify_api.test.view.track.input.attributes_source.data.FieldFromDataTestCase import NonNullableStrFieldFromDataTestCase


class TitleTestCase(NonNullableStrFieldFromDataTestCase):
    post_field_key = POST_FIELDS.TITLE

    def test_value_then_ok(self):
        value = 'fr'
        data = {POST_FIELDS.TITLE: value}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.title == value
