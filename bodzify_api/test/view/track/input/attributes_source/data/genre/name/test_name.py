#!/usr/bin/env python

import pytest

from bodzify_api.test import conftest
from bodzify_api.test.view.track.input.attributes_source.data.genre.name.TestCase import TestCase


@pytest.fixture(params=[TestCase])
def childinstance(request, db):
    yield from conftest.base_childinstance(request, db)
