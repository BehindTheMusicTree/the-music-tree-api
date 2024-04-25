#!/usr/bin/env python

import pytest
from bodzify_api.test import conftest
from bodzify_api.test.view.track.input.source.data.genre.name.GenreNameTestCase import GenreNameTestCase



@pytest.fixture(params=[GenreNameTestCase])
def child_instance(request, db):
    yield from conftest.base_child_instance(request, db)