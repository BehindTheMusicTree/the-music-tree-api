from django.urls import reverse

from bodzify_api.model.user.User import User
from bodzify_api.test.utils.AppTestCase import AppTestCase


class UserTestCase(AppTestCase[User]):
    model_class = User
    saved_object: User

    def _post_user(self, **kwargs):
        return self.api_client.post(path=reverse('user-list'), data=kwargs, content_type='application/json')

    def _get_users(self):
        return self.api_client.get(path=reverse('user-list'), handle_response=self._set_results)

    def _retrieve_user(self, pk: int):
        return self.api_client.get(path=reverse('user-detail', kwargs={'pk': pk}))

    def _put_user(self, pk: int, **kwargs):
        return self.api_client.put(path=reverse('user-detail', kwargs={'pk': pk}),
                                   data=kwargs,
                                   content_type='application/json',
                                   handle_response=self._set_results)

    def _delete_user(self, pk: int):
        return self.api_client.delete(path=reverse('user-detail', kwargs={'pk': pk}))
