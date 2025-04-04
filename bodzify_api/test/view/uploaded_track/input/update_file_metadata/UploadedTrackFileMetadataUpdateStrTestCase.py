

from rest_framework import status

from bodzify_api.test.view.uploaded_track.input.update_file_metadata.UploadedTrackFileMetadataUpdateTestCase import UploadedTrackFileMetadataUpdateTestCase


class UploadedTrackFileMetadataUpdateStrTestCase(UploadedTrackFileMetadataUpdateTestCase):

    VALUE_EXPECTED_IN_METADATA_WHEN_NOT_PROVIDED = 'LJjksjsksjldkjlksjdlksjkdjskljdslkdjsldslnccsdvkjbvkvb'
    value_expected_in_metadata_is_list = False

    length_max: int

    def _test_value(self,
                    value: str | None,
                    additional_data,
                    value_expected_in_metadata=VALUE_EXPECTED_IN_METADATA_WHEN_NOT_PROVIDED,
                    file_has_metadata=False):
        data = {self.save_field: value}

        if additional_data:
            data.update(additional_data)

        response = self._post_uploaded_track(file_has_metadata=file_has_metadata, extension=self.file_extension, **data)

        assert response.status_code == status.HTTP_201_CREATED

        if value_expected_in_metadata == self.VALUE_EXPECTED_IN_METADATA_WHEN_NOT_PROVIDED:
            value_expected_in_metadata = value

        if value_expected_in_metadata is None:
            if self.uploaded_track_app_metadata_key in self.saved_uploaded_track_metadata_with_raw_rating:
                assert not self.saved_uploaded_track_metadata_with_raw_rating[self.uploaded_track_app_metadata_key]
            else:
                assert True
        else:
            assert self.uploaded_track_app_metadata_key in self.saved_uploaded_track_metadata_with_raw_rating
            metadata_value = self.saved_uploaded_track_metadata_with_raw_rating[self.uploaded_track_app_metadata_key]
            if self.value_expected_in_metadata_is_list:
                if not isinstance(value_expected_in_metadata, list):
                    value_expected_in_metadata = [value_expected_in_metadata]
                assert sorted(metadata_value) == sorted(value_expected_in_metadata)
            else:
                assert len(metadata_value) == len(value_expected_in_metadata)
                assert metadata_value == value_expected_in_metadata

    def test_on_missing_tag_then_ok(self, additional_data=None):
        self._test_value("a", additional_data=additional_data, file_has_metadata=False)

    def test_on_present_tag_then_ok(self, additional_data=None):
        self._test_value("a", additional_data=additional_data, file_has_metadata=True)

    def test_largest_then_ok(self, additional_data=None):
        self._test_value('a' * self.length_max, additional_data=additional_data, file_has_metadata=False)
