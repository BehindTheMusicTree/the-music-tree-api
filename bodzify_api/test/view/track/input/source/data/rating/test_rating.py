#!/usr/bin/env python

import pytest
from bodzify_api.test import conftest
from bodzify_api.test.view.track.input.source.data.rating.RatingTestCase import RatingTestCase


@pytest.fixture(params=[RatingTestCase])
def child_instance(request, db):
    yield from conftest.base_child_instance(request, db)
