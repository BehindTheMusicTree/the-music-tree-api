#!/usr/bin/env python

import pytest
from bodzify_api.test import conftest
from bodzify_api.test.view.track.input.source.data.AttributeFromDataTestCase \
    import ArtistTestCase, GenreTestCase, LanguageTestCase, TitleTestCase, RatingTestCase


@pytest.fixture(params=[ArtistTestCase, GenreTestCase, LanguageTestCase, TitleTestCase, RatingTestCase])
def child_instance(request, db):
    yield from conftest.base_child_instance(request, db)
