from uuid import UUID

from django.urls import reverse

from bodzify_api.model.artist.Artist import Artist
from bodzify_api.test.ApiTestCase import ApiTestCase


class ArtistTestCase(ApiTestCase[Artist]):
    model_class = Artist
    saved_object: Artist

    def _post_artist(self, **kwargs):
        return self.api_client.post(
            path=reverse('artist-list'),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            handle_response=self._set_results
        )

    def _get_artists(self, **kwargs):
        return self.api_client.get(
            path=reverse('artist-list'),
            data=kwargs,
            handle_response=self._set_results_attributes
        )

    def _retrieve_artist(self, uuid: UUID):
        return self.api_client.get(
            path=reverse('artist-detail', kwargs={'pk': uuid}),
            handle_response=self._set_results
        )

    def _put_artist(self, uuid: UUID, **kwargs):
        return self.api_client.put(
            path=reverse('artist-detail', kwargs={'pk': uuid}),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            handle_response=self._set_results
        )

    def _delete_artist(self, uuid: UUID):
        return self.api_client.delete(path=reverse('artist-detail', kwargs={'pk': uuid}))
