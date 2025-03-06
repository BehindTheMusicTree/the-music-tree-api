

from rest_framework import status

from bodzify_api.test.utils.ApiTestCase import ApiTestCase


class TestCase(ApiTestCase):
    def test_not_logged_in_then_401(self):
        response = self._post_lib_track_being_logged_out()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        error = response.json()
