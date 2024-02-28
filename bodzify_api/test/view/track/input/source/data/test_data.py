#!/usr/bin/env python

import pytest
from bodzify_api.test import conftest
from bodzify_api.test.view.track.input.source.data.LibTrackAttributeFromDataTestCase \
    import ArtistTestCase, GenreTestCase, LanguageTestCase, TitleTestCase


@pytest.fixture(params=[ArtistTestCase, GenreTestCase, LanguageTestCase, TitleTestCase])
def child_instance(request, db):
    yield from conftest.base_child_instance(request, db)
