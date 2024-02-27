#!/usr/bin/env python

import logging

import pytest

from bodzify_api.test.view.track.input.source.file_metadata.language.LanguageTestCase \
    import LanguageMp3TestCase, LanguageWavTestCase, LanguageFlacTestCase

logger = logging.getLogger('bodzify_api')


@pytest.fixture(params=[LanguageMp3TestCase, LanguageWavTestCase, LanguageFlacTestCase])
def child_instance(request, db):
    test_case = request.param()
    test_case.setUp()
    yield test_case
    test_case.tearDown()
