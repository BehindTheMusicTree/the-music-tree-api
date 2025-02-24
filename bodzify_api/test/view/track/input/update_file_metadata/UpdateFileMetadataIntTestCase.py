from typing import Optional

from rest_framework import status

from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class UpdateFileMetadataIntTestCase(LibTrackTestCase):
    save_field: Optional[str] = None
    lib_track_app_metadata_key: Optional[str] = None
    file_extension: str
    value_min: Optional[int] = None
    value_max: Optional[int] = None
    value_min_expected_in_metadata: Optional[int] = None
    value_max_expected_in_metadata: Optional[int] = None

    def _test_value(self, value: Optional[int],
                    value_expected_in_metadata: Optional[int] = None,
                    additional_data_=None,
                    file_has_tags=False):
        value_str = str(value) if value else ''
        data = {self.save_field: value_str}
        if additional_data_:
            data.update(additional_data_)

        if file_has_tags:
            response = self._post_lib_track_with_generic_sample_tags_max_length_of_a(
                extension=self.file_extension, **data)
        else:
            response = self._post_lib_track_with_generic_sample_no_tags(
                extension=self.file_extension, **data)

        assert response.status_code == status.HTTP_201_CREATED

        value_expected_in_metadata = value_expected_in_metadata if value_expected_in_metadata else value

        if value_expected_in_metadata is None:
            if self.lib_track_app_metadata_key in self.saved_lib_track_metadata:
                assert not self.saved_lib_track_metadata[self.lib_track_app_metadata_key]
            else:
                assert True
        else:
            assert self.lib_track_app_metadata_key in self.saved_lib_track_metadata
            assert self.saved_lib_track_metadata[self.lib_track_app_metadata_key] == value_expected_in_metadata
