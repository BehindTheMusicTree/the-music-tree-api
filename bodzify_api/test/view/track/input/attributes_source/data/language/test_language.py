import pytest

from bodzify_api.test import conftest
from bodzify_api.test.view.track.input.attributes_source.data.language.LanguageTestCase import     LanguageTestCase


@pytest.fixture(params=[LanguageTestCase])
def childinstance(request, db):
    yield from conftest.base_childinstance(request, db)
