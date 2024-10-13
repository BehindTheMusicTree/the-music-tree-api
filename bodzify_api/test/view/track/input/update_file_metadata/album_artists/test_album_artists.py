#!/usr/bin/env python


import pytest

from bodzify_api.test import conftest
from bodzify_api.test.view.track.input.update_file_metadata.album_artists.TestCase import (
    FlacTestCase, Mp3TestCase, WavTestCase)


@pytest.fixture(params=[Mp3TestCase, WavTestCase, FlacTestCase])
def child_instance(request, db):
    yield from conftest.base_child_instance(request, db)


def test_spacing(child_instance):
    child_instance._test_value(value="Chuck Berry,  The Beatles,the Rolling Stones ",
                               additional_data_dict=child_instance.album_data_dict,
                               value_expected_in_metadata="Chuck Berry,The Beatles,the Rolling Stones",
                               file_has_tags=False)
