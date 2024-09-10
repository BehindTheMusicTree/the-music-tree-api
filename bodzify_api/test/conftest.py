#!/usr/bin/env python

import pytest

critical_test_failed = False


def base_child_instance(request, db):
    test_case = request.param()
    test_case.setUp()
    yield test_case
    test_case.tearDown


def pytest_configure(config):
    config.addinivalue_line("markers", "critical: mark test as critical to pass")


def pytest_runtest_makereport(item, call):
    global critical_test_failed
    critical_marker = item.get_closest_marker("critical")
    if call.when == "call" and critical_marker is not None:
        if call.excinfo is not None:
            critical_test_failed = True
            print(f"CRITICAL TEST FAILED: {item.name}")
            print(f"Output: {call.excinfo}")


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    if critical_test_failed:
        pytest.skip("A critical test has failed. Skipping the rest of the tests..")


def pytest_collection_modifyitems(config, items):
    # Set critical tests first
    critical_tests = []
    non_critical_tests = []

    print("Setting critical tests first")
    for item in items:
        critical_marker = item.get_closest_marker("critical")
        if critical_marker is not None:
            critical_tests.append(item)
        else:
            non_critical_tests.append(item)

    items[:] = critical_tests + non_critical_tests
