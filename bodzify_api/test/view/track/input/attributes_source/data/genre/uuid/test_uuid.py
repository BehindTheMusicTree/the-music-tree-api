#!/usr/bin/env python

import pytest
from bodzify_api.test import conftest

from bodzify_api.test.view.track.input.source.data.genre.uuid.GenreUuidTestCase import GenreUuidTestCase


@pytest.fixture(params=[GenreUuidTestCase])
def child_instance(request, db):
    yield from conftest.base_child_instance(request, db)
