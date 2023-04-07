#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


@pytest.mark.django_db
class FormatTextCase(TrackViewTestCase):

    def test_errorWhenBadFormat(self):
        response = self.postSampleTrack("format_error.wav")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
