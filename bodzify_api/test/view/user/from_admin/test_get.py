from rest_framework import status

from bodzify_api.test.view.user.UserViewTestCase import UserViewTestCase


class TestCase(UserViewTestCase):

    def test_get_then_ok(self):
        self._login_as_test_admin()
        response = self._get_users()
        assert response.status_code == status.HTTP_200_OK
