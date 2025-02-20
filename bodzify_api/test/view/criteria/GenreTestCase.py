from uuid import UUID

from django.urls import reverse

from bodzify_api.model.criteria.children.genre.Genre import Genre
from bodzify_api.serializer.model.criteria.output.Fields import Fields
from bodzify_api.test.ApiTestCase import ApiTestCase


class GenreTestCase(ApiTestCase[Genre]):
    saved_object: Genre
    model_class = Genre

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.detail_endpoint = 'genre-detail'
        self.list_endpoint = 'genre-list'

    def _set_saved_object(self, response):
        """Override base method to add user filter to query."""
        uuid = response.json()[Fields.UUID]
        self.saved_object = self.model_class.objects.get(user=self.test_user1, uuid=uuid)  # type: ignore

    def _retrieve_genre(self, uuid: UUID):
        return self.api_client.get(
            path=reverse(self.detail_endpoint, kwargs={'pk': uuid}),
            handle_response=self._set_results
        )

    def _get_genres(self, **kwargs):
        return self.api_client.get(
            path=reverse(self.list_endpoint),
            data=kwargs,
            handle_response=self._set_results
        )

    def _post_genre(self, **kwargs):
        return self.api_client.post(
            path=reverse(self.list_endpoint),
            data=kwargs,
            content_type='application/json',
            handle_response=self._set_results
        )

    def _put_genre(self, uuid: UUID, **kwargs):
        return self.api_client.put(
            path=reverse(self.detail_endpoint, kwargs={'pk': uuid}),
            data=kwargs,
            content_type='application/json',
            handle_response=self._set_results
        )

    def _delete_genre(self, uuid: UUID):
        return self.api_client.delete(path=reverse(self.detail_endpoint, kwargs={'pk': uuid}))
