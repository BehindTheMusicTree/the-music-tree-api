#!/usr/bin/env python

from rest_framework import status
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_extra_field_then_error(self):
        data = {"field_not_handled": "pofkefposkfwp"}
        response = self.extract_default_mine_track(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore
