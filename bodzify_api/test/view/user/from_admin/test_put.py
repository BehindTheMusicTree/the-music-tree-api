from rest_framework import status

from bodzify_api.test.view.user.UserTestCase import UserTestCase


class TestCase(UserTestCase):

    def test_put_then_ok(self):
        new_email = 'newemail@whatever.com'
        self._login_as_test_admin()
        response = self._put_user(pk=self.test_user1.pk, email=new_email)
        assert response.status_code == status.HTTP_200_OK
        self.test_user1.refresh_from_db()
        assert self.test_user1.email == new_email
