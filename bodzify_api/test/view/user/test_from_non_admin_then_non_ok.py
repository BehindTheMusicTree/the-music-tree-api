from rest_framework import status

from bodzify_api.test.view.user.UserViewTestCase import UserViewTestCase


class TestCase(UserViewTestCase):

    def test_non_admin_then_post_not_allowed(self):
        response = self._post_user()
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_non_admin_then_put_not_allowed(self):
        response = self._put_user(pk=1)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_non_admin_then_delete_not_allowed(self):
        response = self._delete_user(pk=1)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_non_admin_then_retrieve_not_allowed(self):
        response = self._retrieve_user(pk=1)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
