from uuid import UUID

from django.urls import reverse

from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.test.utils.AppTestCase import AppTestCase
from bodzify_api.test.utils.lib_track.LibTrackTestUrl import LibTracTestkUrl
from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields


class LibTrackTestCase(AppTestCase[LibraryTrack]):
    model_class = LibraryTrack
    saved_object: LibraryTrack

    def _post_lib_track_from_url(self, test_lib_track_url: LibTracTestkUrl = LibTracTestkUrl.MP3, **kwargs):
        kwargs[Fields.TRACK_FILE_PUBLIC] = str(test_lib_track_url)
        return self.api_client.post(
            path=reverse('library-track-list'), data=kwargs, handle_response=self._set_results)

    def _post_lib_track_without_file(self, **kwargs):
        return self.api_client.post(
            path=reverse('library-track-list'), data=kwargs, handle_response=self._set_results)

    def _download_lib_track(self, uuid):
        return self.api_client.get(path=reverse('library-track-download', kwargs={'pk': uuid}))

    def _delete_lib_track(self, uuid):
        return self.api_client.delete(path=reverse('library-track-detail', kwargs={'pk': uuid}))

    def _retrieve_lib_track(self, uuid: UUID):
        return self.api_client.get(path=reverse('library-track-detail', kwargs={'pk': uuid}),
                                   handle_response=self._set_results)

    def _list_lib_tracks(self, **kwargs):
        return self.api_client.get(path=reverse('library-track-list'), data=kwargs, handle_response=self._set_results)
