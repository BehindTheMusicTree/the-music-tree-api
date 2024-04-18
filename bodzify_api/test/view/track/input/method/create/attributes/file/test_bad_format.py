#!/usr/bin/env python

import pytest
from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


@pytest.mark.django_db
class FormatTextCase(TrackTestCase):

    def test_bad_format_then_error(self):
        response = self.post_lib_track_with_specific_sample("bad_format.wav")
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore
