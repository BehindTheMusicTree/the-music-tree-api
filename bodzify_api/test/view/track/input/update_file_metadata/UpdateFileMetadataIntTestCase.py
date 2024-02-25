#!/usr/bin/env python

from abc import ABC
from typing import Optional
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from rest_framework import status


class UpdateFileMetadataIntTestCase(ApiViewTestCase, ABC):
    save_field: str
    metadata_dict_key: str
    file_extension: str
    value_min: int
    value_max: int
    value_min_in_metadata: int
    value_max_in_metadata: int

    def _test_value(self, value: Optional[int],
                    value_in_matadata: Optional[int] = None,
                    additional_data_json=None,
                    file_has_tags=False):
        value_str = str(value) if value is not None else ''
        data = {
            self.save_field: value_str
        }
        if additional_data_json:
            data.update(additional_data_json)

        if file_has_tags:
            response = self.post_lib_track_with_generic_sample_tags_max_length_of_a(
                generic_sample_extension=self.file_extension, data_json=data)
        else:
            response = self.post_lib_track_with_generic_sample_no_tags(
                generic_sample_extension=self.file_extension, data_json=data)

        assert response.status_code == status.HTTP_201_CREATED

        value_in_matadata = value_in_matadata if value_in_matadata is not None else value

        if value_in_matadata is None:
            assert self.saved_lib_track_metadata[self.metadata_dict_key] in ["", None]
        else:
            assert self.saved_lib_track_metadata[self.metadata_dict_key] == value_in_matadata

    def test_on_missing_tag_then_ok(self, additional_data_json=None):
        self._test_value(value=self.value_min,
                         value_in_matadata=self.value_min_in_metadata,
                         additional_data_json=additional_data_json,
                         file_has_tags=False)

    def test_on_present_tag_then_ok(self, additional_data_json=None):
        self._test_value(value=self.value_min,
                         value_in_matadata=self.value_min_in_metadata,
                         additional_data_json=additional_data_json,
                         file_has_tags=True)

    def test_max_then_ok(self, additional_data_json=None):
        self._test_value(value=self.value_max,
                         value_in_matadata=self.value_max_in_metadata,
                         additional_data_json=additional_data_json,
                         file_has_tags=False)

    def test_min_then_ok(self, additional_data_json=None):
        self._test_value(value=self.value_min,
                         value_in_matadata=self.value_min_in_metadata,
                         additional_data_json=additional_data_json,
                         file_has_tags=False)

    def test_none_then_none(self, additional_data_json=None):
        self._test_value(value=None, additional_data_json=additional_data_json, file_has_tags=False)
