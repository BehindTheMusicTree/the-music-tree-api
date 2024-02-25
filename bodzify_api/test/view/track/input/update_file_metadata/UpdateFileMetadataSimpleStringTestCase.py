#!/usr/bin/env python

from rest_framework import status

from bodzify_api.test.view.track.input.update_file_metadata.UpdateFileMetadataStringTestCase import \
    UpdateFileMetadataStringTestCase


class UpdateFileMetadataSimpleStringTestCase(UpdateFileMetadataStringTestCase):

    def __init__(self,
                 save_field: str,
                 metadata_dict_key: str,
                 file_extension: str,
                 length_max: int,
                 methodName: str = "runTest") -> None:
        self.save_field = save_field
        self.metadata_dict_key = metadata_dict_key
        self.file_extension = file_extension
        self.length_max = length_max
        super().__init__(methodName)

    def test_on_missing_tag_then_ok(self):
        value = "a"
        data = {
            self.save_field: value
        }
        response = self.post_lib_track_with_generic_sample_no_tags(
            generic_sample_extension=self.file_extension, data_json=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track_metadata[self.metadata_dict_key] == value

    def test_on_present_tag_then_ok(self):
        value = "a"
        data = {
            self.save_field: value
        }
        response = self.post_lib_track_with_generic_sample_tags_max_length_of_a(
            generic_sample_extension=self.file_extension, data_json=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track_metadata[self.metadata_dict_key] == value

    def test_longest_then_ok(self):
        value = "a" * self.length_max
        data = {
            self.save_field: value
        }
        response = self.post_lib_track_with_generic_sample_no_tags(
            generic_sample_extension=self.file_extension, data_json=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track_metadata[self.metadata_dict_key] == value

    def test_none_then_none(self):
        data = {
            self.save_field: ""
        }
        response = self.post_lib_track_with_generic_sample_no_tags(
            generic_sample_extension=self.file_extension, data_json=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track_metadata[self.metadata_dict_key] in ["", None]
