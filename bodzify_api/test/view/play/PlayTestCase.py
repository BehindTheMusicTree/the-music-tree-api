from uuid import UUID

from django.urls import reverse

from bodzify_api.model.play.Play import Play
from bodzify_api.test.ApiTestCase import ApiTestCase


class PlayTestCase(ApiTestCase[Play]):
    model_class = Play
    saved_object: Play

    def _post_play(self, **kwargs):
        return self.api_client.post(
            path=reverse('play-list'),
            data=kwargs,
            content_type='application/json',
            handle_response=self._set_results
        )

    def _get_plays(self, **kwargs):
        return self.api_client.get(
            path=reverse('play-list'),
            data=kwargs,
            handle_response=self._set_results
        )

    def _put_play(self, play_uuid: UUID, **kwargs):
        return self.api_client.put(
            path=reverse('play-detail', kwargs={'pk': play_uuid}),
            data=kwargs,
            content_type='application/json',
            handle_response=self._set_results
        )

    def _delete_play(self, uuid: UUID):
        return self.api_client.delete(path=reverse('play-detail', kwargs={'pk': uuid}))
