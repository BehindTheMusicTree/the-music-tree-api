#!/usr/bin/env python

import pytest

from bodzify_api.test import conftest
from bodzify_api.test.view.track.input.attributes_source.data.title.TitleTestCase import \
    TitleTestCase


@pytest.fixture(params=[TitleTestCase])
def child_instance(request, db):
    yield from conftest.base_child_instance(request, db)
