#!/usr/bin/env python

from typing import Optional
from venv import logger
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from rest_framework import status


class UpdateFileMetadataStrTestCase(ApiViewTestCase):

    VALUE_EXPECTED_IN_METADATA_NOT_PROVIDED = 'LJjksjsksjldkjlksjdlksjkdjskljdslkdjsldslnccsdvkjbvkvb'

    save_field = None
    lib_track_metadata_dict_key = None
    file_extension = None
    length_max = None

    def _test_value(
            self,
            value: Optional[str],
            additional_data_json,
            value_expected_in_metadata=VALUE_EXPECTED_IN_METADATA_NOT_PROVIDED,
            file_has_tags=False):
        data = {
            self.save_field: value
        }

        if additional_data_json:
            data.update(additional_data_json)

        if file_has_tags:
            response = self.post_lib_track_with_generic_sample_tags_max_length_of_a(
                extension=self.file_extension, data_json=data)
        else:
            response = self.post_lib_track_with_generic_sample_no_tags(
                extension=self.file_extension, data_json=data)  # type: ignore
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore

        if value_expected_in_metadata == self.VALUE_EXPECTED_IN_METADATA_NOT_PROVIDED:
            value_expected_in_metadata = value

        if value_expected_in_metadata is None:
            if self.lib_track_metadata_dict_key in self.saved_lib_track_metadata:
                assert self.saved_lib_track_metadata[self.lib_track_metadata_dict_key] in ["", None]
            else:
                assert True
        else:
            assert self.lib_track_metadata_dict_key in self.saved_lib_track_metadata
            assert self.saved_lib_track_metadata[self.lib_track_metadata_dict_key] == value_expected_in_metadata

    def test_on_missing_tag_then_ok(self, additional_data_json=None):
        self._test_value("a", additional_data_json=additional_data_json, file_has_tags=False)

    def test_on_present_tag_then_ok(self, additional_data_json=None):
        self._test_value("a", additional_data_json=additional_data_json, file_has_tags=True)

    def test_longest_then_ok(self, additional_data_json=None):
        self._test_value(
            "a" * self.length_max, additional_data_json=additional_data_json, file_has_tags=False)  # type: ignore
