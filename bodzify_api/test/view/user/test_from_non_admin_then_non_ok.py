from rest_framework import status

from bodzify_api.test.view.user.UserTestCase import UserTestCase


class TestCase(UserTestCase):

    def test_non_admin_then_post_403(self):
        response = self._post_user()
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_non_admin_then_put_403(self):
        response = self._put_user(pk=1)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_non_admin_then_delete_403(self):
        response = self._delete_user(pk=1)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_non_admin_then_retrieve_not_403(self):
        response = self._retrieve_user(pk=1)
        assert response.status_code == status.HTTP_403_FORBIDDEN
