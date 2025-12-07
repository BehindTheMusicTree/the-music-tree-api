from uuid import UUID

from django.urls import reverse

from api.model.playlist.children.criteria.tag.TagPlaylist import TagPlaylist
from api.test.utils.AppTestCase import AppTestCase


class TagPlaylistTestCase(AppTestCase):
    model_class = TagPlaylist
    saved_object: TagPlaylist

    def _post_tag_playlist(self, **kwargs):
        return self.api_client.post(path=reverse('tag-playlist-list'),
                                    data=kwargs,
                                    content_type='application/json',
                                    handle_response=self._set_results)

    def _retrieve_tag_playlist(self, uuid):
        return self.api_client.get(
            path=reverse('tag-playlist-detail', kwargs={'pk': uuid}), handle_response=self._set_results)

    def _list_tag_playlists(self, **kwargs):
        return self.api_client.get(
            path=reverse('tag-playlist-list'), data=kwargs, handle_response=self._set_results)

    def _put_tag_playlist(self, uuid: UUID, **kwargs):
        return self.api_client.put(path=reverse('tag-playlist-detail', kwargs={'pk': uuid}),
                                   data=kwargs,
                                   content_type='application/json',
                                   handle_response=self._set_results)

    def _delete_tag_playlist(self, uuid):
        return self.api_client.delete(path=reverse('tag-playlist-detail', kwargs={'pk': uuid}))
