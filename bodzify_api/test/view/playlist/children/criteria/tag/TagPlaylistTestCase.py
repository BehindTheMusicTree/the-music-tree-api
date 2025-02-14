from uuid import UUID
from django.urls import reverse

from bodzify_api.test.ApiTestCase import ApiTestCase


class TagPlaylistTestCase(ApiTestCase):

    def _post_tag_playlist(self, **kwargs):
        return self.api_client.post(
            path=reverse('tag-playlist-list'),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            handle_response=self._set_results
        )

    def _retrieve_tag_playlist(self, uuid):
        return self.api_client.get(
            path=reverse('tag-playlist-detail', kwargs={'pk': uuid}),
            handle_response=self._set_results
        )

    def _get_tag_playlists(self, **kwargs):
        return self.api_client.get(
            path=reverse('tag-playlist-list'),
            data=kwargs,
            handle_response=self._set_results
        )

    def _put_tag_playlist(self, uuid: UUID, **kwargs):
        return self.api_client.put(
            path=reverse('tag-playlist-detail', kwargs={'pk': uuid}),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            handle_response=self._set_results
        )

    def _delete_tag_playlist(self, uuid):
        return self.api_client.delete(path=reverse('tag-playlist-detail', kwargs={'pk': uuid}))
