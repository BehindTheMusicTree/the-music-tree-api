
import pytest

from bodzify_api.test import conftest
from bodzify_api.test.view.track.input.attributes_source.data.rating.RatingTestCase import \
    RatingTestCase


@pytest.fixture(params=[RatingTestCase])
def childinstance(request, db):
    yield from conftest.base_childinstance(request, db)
