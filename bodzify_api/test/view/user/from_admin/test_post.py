from rest_framework import status

from bodzify_api.serializer.schema.user.input.Fields import Fields
from bodzify_api.test.view.user.UserTestCase import UserTestCase


class TestCase(UserTestCase):

    def test_post_then_not_allowed(self):
        data = {Fields.USERNAME: 'test', Fields.PASSWORD: 'test', Fields.EMAIL: 'john@gmail.com'}
        response = self._post_user(kwargs=data)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
