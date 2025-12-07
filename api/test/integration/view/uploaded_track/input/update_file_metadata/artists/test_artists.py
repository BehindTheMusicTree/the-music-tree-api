import pytest

from api.test import conftest
from api.test.integration.view.uploaded_track.input.update_file_metadata.artists.TestCase import (
    FlacTestCase,
    Mp3TestCase,
    WavTestCase
)


@pytest.fixture(params=[Mp3TestCase, WavTestCase, FlacTestCase])
def childinstance(request, db):
    yield from conftest.base_childinstance(request, db)


def test_3_then_ok(childinstance):
    childinstance._test_value(value=["artist1", "artist2", "artist3"],
                              value_expected_in_metadata=["artist1", "artist2", "artist3"],
                              additional_data=None,
                              file_has_metadata=False)
