#!/usr/bin/env python

import logging

import pytest

from bodzify_api.test import conftest
from bodzify_api.test.view.track.input.update_file_metadata.title.TestCase \
    import Mp3TestCase, WavTestCase, FlacTestCase


@pytest.fixture(params=[Mp3TestCase, WavTestCase, FlacTestCase])
def child_instance(request, db):
    yield from conftest.base_child_instance(request, db)
