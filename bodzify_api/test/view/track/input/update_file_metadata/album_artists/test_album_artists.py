

import pytest

from bodzify_api.test import conftest
from bodzify_api.test.view.track.input.update_file_metadata.album_artists.TestCase import (
    FlacTestCase, Mp3TestCase, WavTestCase)


@pytest.fixture(params=[Mp3TestCase, WavTestCase, FlacTestCase])
def childinstance(request, db):
    yield from conftest.base_childinstance(request, db)


def test_spacing(childinstance):
    childinstance._test_value(value="Chuck Berry,  The Beatles,the Rolling Stones ",
                              additional_data_dict=childinstance.album_data_dict,
                              value_expected_in_metadata="Chuck Berry,The Beatles,the Rolling Stones",
                              file_has_tags=False)
