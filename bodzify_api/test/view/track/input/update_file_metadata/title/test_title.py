import pytest

from bodzify_api.test import conftest
from bodzify_api.test.view.track.input.update_file_metadata.title.TestCase import (
    FlacTestCase, Mp3TestCase, WavTestCase)


@pytest.fixture(params=[Mp3TestCase, WavTestCase, FlacTestCase])
def childinstance(request, db):
    yield from conftest.base_childinstance(request, db)
