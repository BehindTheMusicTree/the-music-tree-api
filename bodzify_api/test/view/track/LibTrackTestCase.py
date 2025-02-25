from uuid import UUID

from django.urls import reverse

from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.serializer.model.lib_track.input.extract.Fields import \
    Fields as LibTrackExtractFields
from bodzify_api.test.ApiTestCase import ApiTestCase
from bodzify_api.utils import data_transformer


class LibTrackTestCase(ApiTestCase[LibraryTrack]):
    model_class = LibraryTrack
    saved_object: LibraryTrack

    LIB_TRACK_QUEENSHOWMUSTGOON_FILENAME_WITH_EXTENSION = "queen_showmustgoon 177s.mp3"
    LIB_TRACK_CALIFORNIAGURLS_FLAC_FILENAME_WITH_ID3V2_TAGS_WITH_EXTENSION = "California Gurls with id3v2 tags.flac"
    SKIPPING_TEST_DUE_TO_ACOUSTID_UNKNOWN_CONNECTION_ISSUE = "Skipping test due to Acoustid unknown connection issue."

    class LibTrackGenericSamplesTagsNoneSizeInMo:
        WAV = round(79 / 1000, 2)
        MP3 = round(14 / 1000, 2)
        FLAC = round(51 / 1000, 2)

    class SampleMineTrackUrls:
        WAV = "http://www.canadianmusicartists.com/sample/fx02.wav"
        MP3 = "https://lasonotheque.org/UPLOAD/mp3/0001.mp3"

    SAMPLE_MINE_TRACK_DEFAULT_URL = SampleMineTrackUrls.MP3
    SAMPLE_MINE_TRACK_DEFAULT_EXTENSION = SAMPLE_MINE_TRACK_DEFAULT_URL.split('.')[-1]

    SAMPLE_LIB_TRACK_WAV_DURATION = 1
    SAMPLE_LIB_TRACK_MP3_DURATION = 1
    SAMPLE_LIB_TRACK_FLAC_DURATION = 1

    def _extract(self, **kwargs):
        return self.api_client.post(
            path=reverse('library-track-extract'),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            handle_response=self._set_results
        )

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
            path=reverse('library-track-list'),
            data=kwargs,
            format='json',
            handle_response=self._set_results
        )

    def _post_lib_track_with_queenshowmustgoon(self, **kwargs):
        filename_with_extension = self.LIB_TRACK_QUEENSHOWMUSTGOON_FILENAME_WITH_EXTENSION
        generic_sample_abs_path = self.generic_sample_dir_abs_path / filename_with_extension
        return self._post_lib_track(file_abs_path=generic_sample_abs_path, **kwargs)

    def _post_lib_track_with_californiagurls_flac_with_id3v2_tags(self, **kwargs):
        filename_with_extension = self.LIB_TRACK_CALIFORNIAGURLS_FLAC_FILENAME_WITH_ID3V2_TAGS_WITH_EXTENSION
        generic_sample_abs_path = self.generic_sample_dir_abs_path / filename_with_extension
        return self._post_lib_track(file_abs_path=generic_sample_abs_path, **kwargs)

    def _post_lib_track_with_generic_sample_tag_3_artists_and_two_commas_in_artist(self, extension='mp3', **kwargs):
        filename_without_extension = \
            self.LibTrackGenericSamplesFilenameWithoutExtension.TAGS_3_ARTISTS_AND_2_COMMAS_IN_ARTIST
        return self._post_lib_track_with_generic_sample(
            generic_sample_filename_without_extension=filename_without_extension,
            generic_sample_file_extension=extension,
            **kwargs)

    def _post_lib_track_with_generic_sample_tag_album_koko_without_album_artists(self, extension='mp3', **kwargs):
        filename_without_extension = \
            self.LibTrackGenericSamplesFilenameWithoutExtension.TAGS_ALBUM_KOKO_WITHOUT_ALBUM_ARTISTS
        return self._post_lib_track_with_generic_sample(
            generic_sample_filename_without_extension=filename_without_extension,
            generic_sample_file_extension=extension,
            **kwargs)

    def _post_lib_track_with_generic_sample_tag_album_artists_koko_without_album(self, **kwargs):
        filename_without_extension = \
            self.LibTrackGenericSamplesFilenameWithoutExtension.TAGS_ALBUM_ARTISTS_KOKO_WITHOUT_ALBUM
        return self._post_lib_track_with_generic_sample(
            generic_sample_filename_without_extension=filename_without_extension,
            generic_sample_file_extension='mp3',
            **kwargs)

    def _post_lib_track_with_generic_sample_tags_max_length_of_a(self, extension='mp3', **kwargs):
        filename_without_extension = self.LibTrackGenericSamplesFilenameWithoutExtension.TAGS_MAX_LEN_WITH_LETTER_A
        return self._post_lib_track_with_generic_sample(
            generic_sample_filename_without_extension=filename_without_extension,
            generic_sample_file_extension=extension,
            **kwargs)

    def _post_lib_track_with_generic_sample_1_star(self, extension='mp3', **kwargs):
        filename_without_extension = self.LibTrackGenericSamplesFilenameWithoutExtension.ONE_STAR
        return self._post_lib_track_with_generic_sample(
            generic_sample_filename_without_extension=filename_without_extension,
            generic_sample_file_extension=extension,
            **kwargs)

    def _post_lib_track_with_generic_sample_1_sec(self, **kwargs):
        filename_without_extension = self.LibTrackGenericSamplesFilenameWithoutExtension.BELOW_1_SEC
        return self._post_lib_track_with_generic_sample(
            generic_sample_filename_without_extension=filename_without_extension,
            generic_sample_file_extension='mp3',
            **kwargs)

    def _put_lib_track(self, uuid, **kwargs):
        return self.api_client.put(
            path=reverse('library-track-detail', kwargs={'pk': uuid}),
            data=kwargs,
            handle_response=self._set_results
        )

    def _download_lib_track(self, uuid):
        return self.api_client.get(path=reverse('library-track-download', kwargs={'pk': uuid}))

    def _delete_lib_track(self, uuid):
        return self.api_client.delete(path=reverse('library-track-detail', kwargs={'pk': uuid}))

    def _retrieve_lib_track(self, uuid: UUID):
        return self.api_client.get(
            path=reverse('library-track-detail', kwargs={'pk': uuid}),
            handle_response=self._set_results
        )

    def _get_lib_tracks(self, **kwargs):
        return self.api_client.get(
            path=reverse('library-track-list'),
            data=kwargs,
            handle_response=self._set_results
        )
