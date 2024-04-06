#!/usr/bin/env python

from rest_framework import status
from bodzify_api.serializer.track.input.schema.endpoint.LibTrackPostSerializer import FIELDS as POST_FIELDS
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_uuid_and_name_fields_then_error(self):
        data = {
            POST_FIELDS.GENRE_NAME: 'd',
            POST_FIELDS.GENRE_UUID: 'k' * 22,
        }
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore
