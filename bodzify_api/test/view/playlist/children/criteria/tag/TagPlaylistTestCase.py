from uuid import UUID
from django.urls import reverse
from rest_framework import status

from bodzify_api.test.ApiTestCase import ApiTestCase


class TagPlaylistTestCase(ApiTestCase):

    def _post_tag_playlist(self, **kwargs):
        response = self.api_client.post(path=reverse('tag-playlist-list'),
                                        data=kwargs,
                                        content_type='application/x-www-form-urlencoded')
        if response.status_code == status.HTTP_201_CREATED:
            self._set_result(response)
        return response

    def _retrieve_tag_playlist(self, uuid):
        response = self.api_client.get(path=reverse('tag-playlist-detail', kwargs={'pk': uuid}))
        if response.status_code == status.HTTP_200_OK:
            self._set_result(response)
        return response

    def _get_tag_playlists(self, **kwargs):
        response = self.api_client.get(path=reverse('tag-playlist-list'), data=kwargs)
        if response.status_code == status.HTTP_200_OK:
            self._set_results_attributes(response)
        return response

    def _put_tag_playlist(self, uuid: UUID, **kwargs):
        response = self.api_client.put(path=reverse('tag-playlist-detail', kwargs={'pk': uuid}),
                                       data=kwargs,
                                       content_type='application/x-www-form-urlencoded')
        return response

    def _delete_tag_playlist(self, uuid):
        return self.api_client.delete(path=reverse('tag-playlist-detail', kwargs={'pk': uuid}))
