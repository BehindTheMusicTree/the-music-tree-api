#!/usr/bin/env python

import logging
import pytest

logger = logging.getLogger('bodzify_api')


def base_child_instance(request, db):
    test_case = request.param()
    test_case.setUp()
    yield test_case
    test_case.tearDown()
