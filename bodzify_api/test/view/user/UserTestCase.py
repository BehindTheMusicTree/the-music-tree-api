from django.urls import reverse

from bodzify_api.model.user.User import User
from bodzify_api.test.ApiTestCase import ApiTestCase


class UserTestCase(ApiTestCase[User]):
    def _post_user(self, **kwargs):
        return self.api_client.post(
            path=reverse('user-list'),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            handle_response=self._set_results
        )

    def _get_users(self):
        return self.api_client.get(
            path=reverse('user-list'),
            handle_response=self._set_results
        )

    def _retrieve_user(self, pk: int):
        return self.api_client.get(
            path=reverse('user-detail', kwargs={'pk': pk}),
            handle_response=self._set_results
        )

    def _put_user(self, pk: int, **kwargs):
        return self.api_client.put(
            path=reverse('user-detail', kwargs={'pk': pk}),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            handle_response=self._set_results
        )

    def _delete_user(self, pk: int):
        return self.api_client.delete(path=reverse('user-detail', kwargs={'pk': pk}))
