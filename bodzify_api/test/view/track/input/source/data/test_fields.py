#!/usr/bin/env python

import pytest
from bodzify_api.test import conftest
from bodzify_api.test.view.track.input.source.data.FieldFromDataTestCase import AlbumArtistsTestCase, AlbumTestCase, ArtistTestCase, GenreTestCase, LanguageTestCase, RatingTestCase, TitleTestCase


@pytest.fixture(params=[TitleTestCase,
                        AlbumTestCase,
                        AlbumArtistsTestCase,
                        ArtistTestCase,
                        GenreTestCase,
                        LanguageTestCase,
                        RatingTestCase])
def child_instance(request, db):
    yield from conftest.base_child_instance(request, db)
