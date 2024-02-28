#!/usr/bin/env python

import logging

import pytest

from bodzify_api.test import conftest
from bodzify_api.test.view.track.input.update_file_metadata.rating.RatingTestCase import \
    FlacTestCase, Mp3TestCase, WavTestCase

logger = logging.getLogger('bodzify_api')


@pytest.fixture(params=[Mp3TestCase, WavTestCase, FlacTestCase])
def child_instance(request, db):
    yield from conftest.base_child_instance(request, db)


def test_max_then_ok(child_instance):
    child_instance._test_value(value=child_instance.value_max,
                               value_expected_in_metadata=child_instance.value_max_expected_in_metadata,
                               additional_data_json=None,
                               file_has_tags=False)


def test_on_missing_tag_then_ok(child_instance):
    child_instance._test_value(value=child_instance.value_min,
                               value_expected_in_metadata=child_instance.value_min_expected_in_metadata,
                               additional_data_json=None,
                               file_has_tags=False)


def test_on_present_tag_then_ok(child_instance):
    child_instance._test_value(value=child_instance.value_min,
                               value_expected_in_metadata=child_instance.value_min_expected_in_metadata,
                               additional_data_json=None,
                               file_has_tags=True)


def test_min_then_ok(child_instance):
    child_instance._test_value(value=child_instance.value_min,
                               value_expected_in_metadata=child_instance.value_min_expected_in_metadata,
                               file_has_tags=False)


def test_none_then_none(child_instance):
    child_instance._test_value(value=None, additional_data_json=None, file_has_tags=False)


def test_zero_then_0(child_instance):
    child_instance._test_value(0, 0)
