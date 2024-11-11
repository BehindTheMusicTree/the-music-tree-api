
from urllib.parse import urlencode
from uuid import UUID

from django.urls import reverse
from rest_framework import status

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.schema.playlist.children.manual.output.detailed import Fields as ManualPlaylistGetFields
from bodzify_api.test.ApiTestCase import ApiTestCase


class GenreTestCase(ApiTestCase):
    saved_genre: Criteria

    def _set_saved_genre_attribute(self, response):
        uuid = response.json()[ManualPlaylistGetFields.UUID]
        self.saved_genre = Criteria.objects.get(user=self.test_user1, uuid=uuid)

    def _retrieve_genre(self, uuid: UUID):
        response = self.api_client.get(path=reverse('genre-detail', kwargs={'pk': uuid}))
        if response.status_code == status.HTTP_200_OK:
            self._set_result(response=response)
        return response

    def _get_genres(self, **kwargs):
        response = self.api_client.get(path=reverse('genre-list'), data=kwargs)
        if response.status_code == status.HTTP_200_OK:
            self._set_results_attributes(response)
        return response

    def _post_genre(self, **kwargs):
        data_url_encoded = urlencode(self._replace_none_values_by_empty_string(kwargs), doseq=True)
        response = self.api_client.post(path=reverse('genre-list'),
                                        data=data_url_encoded,
                                        content_type='application/x-www-form-urlencoded')
        if response.status_code == status.HTTP_201_CREATED:
            self._set_saved_genre_attribute(response)
        return response

    def _put_genre(self, uuid: UUID, **kwargs):
        data_url_encoded = urlencode(self._replace_none_values_by_empty_string(kwargs), doseq=True)
        response = self.api_client.put(path=reverse('genre-detail', kwargs={'pk': uuid}),
                                       data=data_url_encoded,
                                       content_type='application/x-www-form-urlencoded')
        if response.status_code == status.HTTP_200_OK:
            self._set_saved_genre_attribute(response)
        return response

    def _delete_genre(self, uuid: UUID):
        return self.api_client.delete(path=reverse('genre-detail', kwargs={'pk': uuid}))
