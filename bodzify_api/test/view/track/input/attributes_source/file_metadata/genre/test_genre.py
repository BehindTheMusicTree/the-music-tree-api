#!/usr/bin/env python

import logging

import pytest

from bodzify_api.test import conftest
from bodzify_api.test.view.track.input.attributes_source.file_metadata.genre.TestCase \
    import Mp3TestCase, WavTestCase, FlacTestCase

logger = logging.getLogger('bodzify_api')


@pytest.fixture(params=[Mp3TestCase, WavTestCase, FlacTestCase])
def child_instance(request, db):
    yield from conftest.base_child_instance(request, db)
