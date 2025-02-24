import pytest

from bodzify_api.test import conftest
from bodzify_api.test.view.track.input.update_file_metadata.rating.TestCase \
    import FlacTestCase, Mp3TestCase, WavTestCase


@pytest.fixture(params=[Mp3TestCase, WavTestCase, FlacTestCase])
def childinstance(request, db):
    yield from conftest.base_childinstance(request, db)


def test_max_then_ok(childinstance):
    childinstance._test_value(value=childinstance.value_max,
                              value_expected_in_metadata=childinstance.value_max_expected_in_metadata,
                              additional_data_dict=None,
                              file_has_tags=False)


def test_on_missing_tag_then_ok(childinstance):
    childinstance._test_value(value=childinstance.value_min,
                              value_expected_in_metadata=childinstance.value_min_expected_in_metadata,
                              additional_data_dict=None,
                              file_has_tags=False)


def test_on_present_tag_then_ok(childinstance):
    childinstance._test_value(value=childinstance.value_min,
                              value_expected_in_metadata=childinstance.value_min_expected_in_metadata,
                              additional_data_dict=None,
                              file_has_tags=True)


def test_min_then_ok(childinstance):
    childinstance._test_value(value=childinstance.value_min,
                              value_expected_in_metadata=childinstance.value_min_expected_in_metadata,
                              file_has_tags=False)


def test_none_then_none(childinstance):
    childinstance._test_value(value=None, additional_data_dict=None, file_has_tags=False)


def test_zero_then_0(childinstance):
    childinstance._test_value(0, 0)
