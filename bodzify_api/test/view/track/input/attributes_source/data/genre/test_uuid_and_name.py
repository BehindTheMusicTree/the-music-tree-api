#!/usr/bin/env python

from rest_framework import status

from bodzify_api import settings
from bodzify_api.serializer.track.input.endpoint.LibTrackPostSerializer import FIELDS as POST_FIELDS
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_uuid_and_name_fields_null_then_none(self):
        data = {
            POST_FIELDS.GENRE_NAME: None,
            POST_FIELDS.GENRE_UUID: None,
        }
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.genre == None

    def test_uuid_and_name_fields_not_both_null_then_error(self):
        data = {
            POST_FIELDS.GENRE_NAME: 'd',
            POST_FIELDS.GENRE_UUID: 'k' * settings.UUID_LEN,
        }
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
