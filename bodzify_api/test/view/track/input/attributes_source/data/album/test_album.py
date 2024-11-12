import pytest

from bodzify_api.test import conftest
from bodzify_api.test.view.track.input.attributes_source.data.album.AlbumTestCase import AlbumTestCase


@pytest.fixture(params=[AlbumTestCase])
def childinstance(request, db):
    yield from conftest.base_childinstance(request, db)
