#!/usr/bin/env python

import pytest
from rest_framework import status
from bodzify_api.test.ApiTestCase import ApiTestCase


@pytest.mark.django_db
class TestCase(ApiTestCase):

    def test_errorWhenMissing(self):
        response = self.post_lib_track_with_specific_sample()
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore
