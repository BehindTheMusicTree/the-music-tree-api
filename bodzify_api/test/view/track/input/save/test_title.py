#!/usr/bin/env python

from rest_framework import status
from bodzify_api import settings
from bodzify_api.serializer.track.input.endpoint.LibTrackPutSerializer import FIELDS as PUT_FIELDS
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_longest_then_ok(self):
        value = "a" * settings.LIB_TRACK_TITLE_LENGTH_MAX
        data = {PUT_FIELDS.TITLE: value}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.title == value

    def test_too_long_then_error(self):
        value = "a" * (settings.LIB_TRACK_TITLE_LENGTH_MAX + 1)
        data = {PUT_FIELDS.TITLE: value}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
