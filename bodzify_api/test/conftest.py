#!/usr/bin/env python

import pytest


def base_child_instance(request, db):
    test_case = request.param()
    test_case.setUp()
    yield test_case
    test_case.tearDown


def pytest_configure(config):
    config.addinivalue_line("markers", "critical: mark test as critical to pass")


def pytest_runtest_makereport(item, call):
    if "critical" in item.keywords:
        if call.excinfo is not None:
            pytest.exit("A critical test failed, stopping the execution of the test suite.")


def pytest_collection_modifyitems(config, items):
    # Set critical tests first
    critical_tests = []
    non_critical_tests = []

    for item in items:
        if "critical" in item.keywords:
            critical_tests.append(item)
        else:
            non_critical_tests.append(item)

    items[:] = critical_tests + non_critical_tests
