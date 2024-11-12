from urllib.parse import urlencode
from uuid import UUID

from django.urls import reverse
from rest_framework import status

from bodzify_api.model.play.Play import Play
from bodzify_api.serializer.schema.play.output.detailed import Fields as OutputFields
from bodzify_api.test.ApiTestCase import ApiTestCase


class PlayTestCase(ApiTestCase):

    def _set_saved_play_attribute(self, response):
        uuid = response.json()[OutputFields.UUID]
        self.saved_play: Play = Play.objects.get(uuid=uuid)

    def _post_play(self, data_dict):
        data_url_encoded = urlencode(self._replace_none_values_by_empty_string(data_dict), doseq=True)
        response = self.api_client.post(path=reverse('play-list'),
                                        data=data_url_encoded,
                                        content_type='application/x-www-form-urlencoded')
        if response.status_code == status.HTTP_201_CREATED:
            self._set_saved_play_attribute(response)
        return response

    def _get_plays(self, **kwargs):
        response = self.api_client.get(path=reverse('play-list'), data=kwargs)
        if response.status_code == status.HTTP_200_OK:
            self._set_results_attributes(response)
        return response

    def _put_play(self, genre_uuid: UUID, data_dict):
        data_url_encoded = urlencode(self._replace_none_values_by_empty_string(**kwargs), doseq=True)
        response = self.api_client.put(path=reverse('play-detail', kwargs={'pk': genre_uuid}),
                                       data=data_url_encoded,
                                       content_type='application/x-www-form-urlencoded')
        if response.status_code == status.HTTP_200_OK:
            self._set_result(response)
        return response

    def _delete_play(self, uuid: UUID):
        return self.api_client.delete(path=reverse('play-detail', kwargs={'pk': uuid}))
