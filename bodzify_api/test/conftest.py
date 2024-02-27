#!/usr/bin/env python

import logging
import pytest

logger = logging.getLogger('bodzify_api')


@pytest.fixture
def child_instance(request, db):
    logger.debug('child_instance')

    def _child_instance(test_case):
        test_case = test_case()
        test_case.setUp()
        yield test_case
        test_case.tearDown()
    return _child_instance
