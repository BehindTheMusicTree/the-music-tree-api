#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.ApiViewTestCase import ApiViewTestCase


@pytest.mark.django_db
class FileMissingTestCase(ApiViewTestCase):

    def test_errorWhenMissing(self):
        response = self.postSampleTrack()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
