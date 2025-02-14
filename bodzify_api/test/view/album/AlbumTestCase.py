from uuid import UUID

from django.urls import reverse

from bodzify_api.model.album.Album import Album
from bodzify_api.test.ApiTestCase import ApiTestCase


class AlbumTestCase(ApiTestCase[Album]):
    def _post_album(self, **kwargs):
        return self.api_client.post(
            path=reverse('album-list'),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            handle_response=self._set_results
        )

    def _get_albums(self, **kwargs):
        return self.api_client.get(
            path=reverse('album-list'),
            data=kwargs,
            handle_response=self._set_results
        )

    def _retrieve_album(self, uuid: UUID):
        return self.api_client.get(
            path=reverse('album-detail', kwargs={'pk': uuid}),
            handle_response=self._set_results
        )

    def _put_album(self, uuid: UUID, **kwargs):
        return self.api_client.put(
            path=reverse('album-detail', kwargs={'pk': uuid}),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            handle_response=self._set_results
        )

    def _delete_album(self, uuid: UUID):
        return self.api_client.delete(path=reverse('album-detail', kwargs={'pk': uuid}))
