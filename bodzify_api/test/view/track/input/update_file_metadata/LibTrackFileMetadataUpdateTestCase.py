

from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class LibTrackFileMetadataUpdateTestCase(LibTrackTestCase):

    VALUE_EXPECTED_IN_METADATA_WHEN_NOT_PROVIDED = 'LJjksjsksjldkjlksjdlksjkdjskljdslkdjsldslnccsdvkjbvkvb'

    save_field: str
    lib_track_app_metadata_key: str
    file_extension: str
    file_extension_metadata_none_test_lib_track_mapping: dict[str, TestLibTrackFilename] = {
        '.mp3': TestLibTrackFilename.METADATA_NONE_MP3,
        '.flac': TestLibTrackFilename.METADATA_NONE_FLAC,
        '.wav': TestLibTrackFilename.METADATA_NONE_WAV
    }
    file_extension_metadata_max_a_test_lib_track_mapping: dict[str, TestLibTrackFilename] = {
        '.mp3': TestLibTrackFilename.METADATA_MAX_A_ID3V2_MP3,
        '.flac': TestLibTrackFilename.METADATA_MAX_A_VORBIS_FLAC,
        '.wav': TestLibTrackFilename.METADATA_MAX_A_ID3V2_WAV
    }

    def _post_lib_track(self, file_has_metadata: bool, extension: str, **data):
        if file_has_metadata:
            return super()._post_lib_track(self.file_extension_metadata_max_a_test_lib_track_mapping[extension], **data)
        else:
            return super()._post_lib_track(self.file_extension_metadata_none_test_lib_track_mapping[extension], **data)

    def _test_value(self, value: str | None,
                    additional_data_dict,
                    value_expected_in_metadata=VALUE_EXPECTED_IN_METADATA_WHEN_NOT_PROVIDED,
                    file_has_metadata=False):
        raise NotImplementedError()
