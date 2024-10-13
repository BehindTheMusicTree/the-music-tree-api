#!/usr/bin/env python


import pytest

from bodzify_api.test import conftest
from bodzify_api.test.view.track.input.attributes_source.file_metadata.album_artists.TestCase import (
    FlacTestCase, Mp3TestCase, WavTestCase)


@pytest.fixture(params=[Mp3TestCase, WavTestCase, FlacTestCase])
def child_instance(request, db):
    yield from conftest.base_child_instance(request, db)
