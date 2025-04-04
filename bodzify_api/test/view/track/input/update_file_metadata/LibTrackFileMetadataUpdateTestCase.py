

from bodzify_api.test.utils.uploaded_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class LibTrackFileMetadataUpdateTestCase(LibTrackTestCase):

    VALUE_EXPECTED_IN_METADATA_WHEN_NOT_PROVIDED = 'LJjksjsksjldkjlksjdlksjkdjskljdslkdjsldslnccsdvkjbvkvb'

    save_field: str
    uploaded_track_app_metadata_key: str
    file_extension: str
    file_extension_metadata_none_test_uploaded_track_mapping: dict[str, LibTrackTestFilename] = {
        '.mp3': LibTrackTestFilename.METADATA_NONE_MP3,
        '.flac': LibTrackTestFilename.METADATA_NONE_FLAC,
        '.wav': LibTrackTestFilename.METADATA_NONE_WAV
    }
    file_extension_metadata_max_a_test_uploaded_track_mapping: dict[str, LibTrackTestFilename] = {
        '.mp3': LibTrackTestFilename.METADATA_LONG_A_ID3V2_SMALL_MP3,
        '.flac': LibTrackTestFilename.METADATA_LONG_A_VORBIS_SMALL_FLAC,
        '.wav': LibTrackTestFilename.METADATA_LONG_A_RIFF_SMALL_WAV
    }

    def _post_uploaded_track(self, file_has_metadata: bool, extension: str, **data):
        if file_has_metadata:
            return super()._post_uploaded_track(
                self.file_extension_metadata_max_a_test_uploaded_track_mapping[extension],
                **data)
        else:
            return super()._post_uploaded_track(
                self.file_extension_metadata_none_test_uploaded_track_mapping[extension],
                **data)

    def _test_value(self, value: str | None,
                    additional_data,
                    value_expected_in_metadata=VALUE_EXPECTED_IN_METADATA_WHEN_NOT_PROVIDED,
                    file_has_metadata=False):
        raise NotImplementedError()
