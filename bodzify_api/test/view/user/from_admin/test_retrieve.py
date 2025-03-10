from rest_framework import status

from bodzify_api.test.view.user.UserTestCase import UserTestCase


class TestCase(UserTestCase):

    def test_retrieve_then_ok(self):
        self._login_as_test_admin()
        response = self._retrieve_user(pk=self.test_user1.pk)
        assert response.status_code == status.HTTP_200_OK
