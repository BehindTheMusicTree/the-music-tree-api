from uuid import UUID

from django.urls import reverse
from rest_framework import status

from bodzify_api.model.play.Play import Play
from bodzify_api.serializer.schema.model.play.output.detailed import Fields as OutputFields
from bodzify_api.test.ApiTestCase import ApiTestCase


class PlayTestCase(ApiTestCase):

    def _set_saved_play_attribute(self, response):
        uuid = response.json()[OutputFields.UUID]
        self.saved_play: Play = Play.objects.get(uuid=uuid)

    def _post_play(self, **kwargs):
        return self.api_client.post(
            path=reverse('play-list'),
            data=kwargs,
            content_type='application/json',
            on_success=self._set_saved_play_attribute
        )

    def _get_plays(self, **kwargs):
        return self.api_client.get(
            path=reverse('play-list'),
            data=kwargs,
            on_success=self._set_results_attributes
        )

    def _put_play(self, genre_uuid: UUID, **kwargs):
        return self.api_client.put(
            path=reverse('play-detail', kwargs={'pk': genre_uuid}),
            data=kwargs,
            content_type='application/json',
            on_success=self._set_result
        )

    def _delete_play(self, uuid: UUID):
        return self.api_client.delete(path=reverse('play-detail', kwargs={'pk': uuid}))
