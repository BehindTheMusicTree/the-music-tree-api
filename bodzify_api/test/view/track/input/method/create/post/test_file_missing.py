#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


@pytest.mark.django_db
class TestCase(ApiViewTestCase):

    def test_errorWhenMissing(self):
        response = self.post_lib_track_with_specific_sample()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
