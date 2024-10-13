#!/usr/bin/env python

import pytest

from bodzify_api.test import conftest
from bodzify_api.test.view.track.input.attributes_source.data.artist.ArtistTestCase import ArtistTestCase


@pytest.fixture(params=[ArtistTestCase])
def child_instance(request, db):
    yield from conftest.base_child_instance(request, db)
