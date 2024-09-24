#!/usr/bin/env python

from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase
from bodzify_api.serializer.track.input.endpoint.post import Fields


class TestCase(TrackTestCase):

    def test_duplicate_fingerprint_and_should_cancel_if_duplicate_fingerprint_then_bad_request(self):
        data = {
            Fields.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT: True
        }
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_not_duplicate_fingerprint_and_should_cancel_if_duplicate_fingerprint_then_ok(self):
        data = {
            Fields.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT: True
        }
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        response = self.post_lib_track_with_queenshowmustgoon(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_duplicate_fingerprint_and_not_should_cancel_if_duplicate_fingerprint_then_ok(self):
        data = {
            Fields.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT: False
        }
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_duplicate_fingerprint_and_should_cancel_if_duplicate_fingerprint_not_provided_then_ok(self):
        data = {
            Fields.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT: False
        }
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
