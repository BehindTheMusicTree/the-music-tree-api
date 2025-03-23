

from rest_framework import status

from bodzify_api.test.view.track.input.update_file_metadata.LibTrackFileMetadataUpdateTestCase import (
    LibTrackFileMetadataUpdateTestCase
)


class LibTrackFileMetadataUpdatePositiveIntTestCase(LibTrackFileMetadataUpdateTestCase):
    value_min: int
    value_max: int
    value_min_expected_in_metadata: int
    value_max_expected_in_metadata: int

    def _test_value(self, value: int | None,
                    value_expected_in_metadata: int | None = None,
                    additional_data=None,
                    file_has_metadata=False):
        value_str = str(value) if value else ''
        data = {self.save_field: value_str}
        if additional_data:
            data.update(additional_data)

        response = self._post_lib_track(file_has_metadata=file_has_metadata, extension=self.file_extension, **data)

        assert response.status_code == status.HTTP_201_CREATED

        value_expected_in_metadata = value_expected_in_metadata if value_expected_in_metadata else value

        if value_expected_in_metadata is None:
            if self.lib_track_app_metadata_key in self.saved_lib_track_metadata_with_raw_rating:
                assert not self.saved_lib_track_metadata_with_raw_rating[self.lib_track_app_metadata_key]
            else:
                assert True
        else:
            assert self.lib_track_app_metadata_key in self.saved_lib_track_metadata_with_raw_rating
            assert self.saved_lib_track_metadata_with_raw_rating[self.lib_track_app_metadata_key] == value_expected_in_metadata
