from uuid import UUID

from django.urls import reverse

from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.serializer.model.lib_track.input.extract.Fields import Fields as LibTrackExtractFields
from bodzify_api.test.utils.ApiTestCase import ApiTestCase
from bodzify_api.utils import data_transformer


class LibTrackTestCase(ApiTestCase[LibraryTrack]):
    model_class = LibraryTrack
    saved_object: LibraryTrack

    class LibTrackGenericSamplesTagsNoneSizeInMo:
        WAV = round(79 / 1000, 2)
        MP3 = round(14 / 1000, 2)
        FLAC = round(51 / 1000, 2)

    class SampleMineTrackUrls:
        WAV = "http://www.canadianmusicartists.com/sample/fx02.wav"
        MP3 = "https://lasonotheque.org/UPLOAD/mp3/0001.mp3"

    SAMPLE_MINE_TRACK_DEFAULT_URL = SampleMineTrackUrls.MP3
    SAMPLE_MINE_TRACK_DEFAULT_EXTENSION = SAMPLE_MINE_TRACK_DEFAULT_URL.split('.')[-1]

    def _extract(self, **kwargs):
        return self.api_client.post(path=reverse('library-track-extract'),
                                    data=kwargs,
                                    content_type='application/x-www-form-urlencoded',
                                    handle_response=self._set_results)

    def _extract_default_mine_track(self, extension=None, **kwargs):
        if extension is None:
            url = self.SAMPLE_MINE_TRACK_DEFAULT_URL
        elif extension == 'wav':
            url = self.SampleMineTrackUrls.WAV
        elif extension == 'mp3':
            url = self.SampleMineTrackUrls.MP3
        else:
            raise ValueError(f"Unknown extension: {extension}")

        extract_data_dict = {LibTrackExtractFields.URL: url}

        if kwargs:
            extract_data_dict = data_transformer.merge_two_dicts(extract_data_dict, kwargs)

        response = self._extract(**extract_data_dict)
        return response

    def _post_lib_track_without_file(self, **kwargs):
        return self.api_client.post(
            path=reverse('library-track-list'), data=kwargs, format='json', handle_response=self._set_results)

    def _put_lib_track(self, uuid, **kwargs):
        return self.api_client.put(
            path=reverse('library-track-detail', kwargs={'pk': uuid}), data=kwargs, handle_response=self._set_results)

    def _download_lib_track(self, uuid):
        return self.api_client.get(path=reverse('library-track-download', kwargs={'pk': uuid}))

    def _delete_lib_track(self, uuid):
        return self.api_client.delete(path=reverse('library-track-detail', kwargs={'pk': uuid}))

    def _retrieve_lib_track(self, uuid: UUID):
        return self.api_client.get(path=reverse('library-track-detail', kwargs={'pk': uuid}),
                                   handle_response=self._set_results)

    def _get_lib_tracks(self, **kwargs):
        return self.api_client.get(path=reverse('library-track-list'), data=kwargs, handle_response=self._set_results)
