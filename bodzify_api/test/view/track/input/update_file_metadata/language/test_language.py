#!/usr/bin/env python

import logging

import pytest

from bodzify_api.test import conftest
from bodzify_api.test.view.track.input.update_file_metadata.language.TestCase \
    import LanguageMp3TestCase, LanguageWavTestCase, LanguageFlacTestCase

logger = logging.getLogger('bodzify_api')


@pytest.fixture(params=[LanguageMp3TestCase, LanguageWavTestCase, LanguageFlacTestCase])
def child_instance(request, db):
    yield from conftest.base_child_instance(request, db)
