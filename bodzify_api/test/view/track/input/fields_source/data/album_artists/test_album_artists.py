#!/usr/bin/env python

import pytest
from bodzify_api.test import conftest
from bodzify_api.test.view.track.input.source.data.album_artists.AlbumArtistsTestCase import AlbumArtistsTestCase


@pytest.fixture(params=[AlbumArtistsTestCase])
def child_instance(request, db):
    yield from conftest.base_child_instance(request, db)
