#!/usr/bin/env python

import os
import shutil
import pytest

from bodzify_api import settings

critical_test_failed = False


def base_childinstance(request, db):
    test_case = request.param()
    test_case.setUp()
    yield test_case
    test_case.tearDown


def pytest_configure(config):
    config.addinivalue_line("markers", "critical: mark test as critical to pass")


def pytest_runtest_makereport(item, call):
    global critical_test_failed
    critical_marker = item.get_closest_marker("critical")
    if call.when == "call" and critical_marker:
        if call.excinfo:
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
        if critical_marker:
            critical_tests.append(item)
        else:
            non_critical_tests.append(item)

    items[:] = critical_tests + non_critical_tests


@pytest.fixture()
def enable_audio_metadata_analysis():
    """Fixture to control metadata analysis during tests."""
    print("Setting up metadata analysis")
    os.environ['AUDIO_META_ANALYSIS_ENABLED_OVERRIDE'] = 'true'
    yield
    os.environ['AUDIO_META_ANALYSIS_ENABLED_OVERRIDE'] = 'false'


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before returning the exit status to the system.
    """
    print("\nExecuting post-test operations...")

    for entry in os.listdir(settings.LIBRARIES_DIR):
        entry_path = os.path.join(settings.LIBRARIES_DIR, entry)
        if os.path.isdir(entry_path) and entry.startswith(settings.TEST_USER_LIBRARIES_DIR_NAME_PREFIXE):
            shutil.rmtree(entry_path)
            print(f"Removed directory: {entry_path}")
