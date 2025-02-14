from uuid import UUID

from django.urls import reverse
from rest_framework import status

from bodzify_api.model.criteria.children.genre.Genre import Genre
from bodzify_api.serializer.schema.model.criteria.output.Fields import Fields
from bodzify_api.test.ApiTestCase import ApiTestCase


class GenreTestCase(ApiTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.detail_endpoint = 'genre-detail'
        self.list_endpoint = 'genre-list'

    def _set_saved_genre_attribute(self, response):
        uuid = response.json()[Fields.UUID]
        self.saved_genre = Genre.objects.get(user=self.test_user1, uuid=uuid)

    def _retrieve_genre(self, uuid: UUID):
        return self.api_client.get(
            path=reverse(self.detail_endpoint, kwargs={'pk': uuid}),
            on_success=self._set_result,
            on_bad_request=self._set_bad_request_result
        )

    def _get_genres(self, **kwargs):
        return self.api_client.get(
            path=reverse(self.list_endpoint),
            data=kwargs,
            on_success=self._set_results_attributes,
            on_bad_request=self._set_bad_request_result
        )

    def _post_genre(self, **kwargs):
        return self.api_client.post(
            path=reverse(self.list_endpoint),
            data=kwargs,
            content_type='application/json',
            on_success=self._set_saved_genre_attribute,
            on_bad_request=self._set_bad_request_result
        )

    def _put_genre(self, uuid: UUID, **kwargs):
        return self.api_client.put(
            path=reverse(self.detail_endpoint, kwargs={'pk': uuid}),
            data=kwargs,
            content_type='application/json',
            on_success=self._set_saved_genre_attribute,
            on_bad_request=self._set_bad_request_result
        )

    def _delete_genre(self, uuid: UUID):
        return self.api_client.delete(path=reverse(self.detail_endpoint, kwargs={'pk': uuid}))
