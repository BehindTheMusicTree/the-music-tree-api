#!/usr/bin/env python

import logging

import pytest

from bodzify_api import AudioMetadataManager
from bodzify_api.test.view.track.input.update_file_metadata.rating.test_case.FlacTestCase import FlacTestCase
from bodzify_api.test.view.track.input.update_file_metadata.rating.test_case.WavTestCase import WavTestCase
from bodzify_api.test.view.track.input.update_file_metadata.rating.test_case.Mp3TestCase import Mp3TestCase
from bodzify_api.serializer.track.input.schema.LibTrackSchemaSaveSerializer import FIELDS as SAVE_FIELDS

logger = logging.getLogger('bodzify_api')


@pytest.fixture(params=[Mp3TestCase, WavTestCase, FlacTestCase])
def child_instance(request, db):
    test_case = request.param()
    test_case.setUp()
    yield test_case
    test_case.tearDown()


def test_max_then_ok(child_instance):
    child_instance._test_value(value=child_instance.value_max,
                               value_in_matadata=child_instance.value_max_in_metadata,
                               additional_data_json=None,
                               file_has_tags=False)


def test_on_missing_tag_then_ok(child_instance):
    child_instance._test_value(value=child_instance.value_min,
                               value_in_matadata=child_instance.value_min_in_metadata,
                               additional_data_json=None,
                               file_has_tags=False)


def test_on_present_tag_then_ok(child_instance):
    child_instance._test_value(value=child_instance.value_min,
                               value_in_matadata=child_instance.value_min_in_metadata,
                               additional_data_json=None,
                               file_has_tags=True)


def test_min_then_ok(child_instance):
    child_instance._test_value(value=child_instance.value_min,
                               value_in_matadata=child_instance.value_min_in_metadata,
                               additional_data_json=None,
                               file_has_tags=False)


def test_none_then_none(child_instance):
    child_instance._test_value(value=None, additional_data_json=None, file_has_tags=False)


def test_zero_then_0(child_instance):
    child_instance._test_value(0, 0)
