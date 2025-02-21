import os
import shutil
from pathlib import Path
from typing import List
import pytest
from _pytest.main import Session

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
            print(f"\nCRITICAL TEST FAILED: {item.name}")
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
def enable_audio_metadata_analysis(request):
    """Control audio metadata analysis state in tests.

    This fixture allows tests to control whether audio metadata analysis is enabled or disabled.
    It can be used in two ways:

    1. As a simple fixture:
       @pytest.fixture(enable_audio_metadata_analysis)
       def test_something():
           # Audio metadata analysis will be enabled

    2. With parametrize to control the state:
       @pytest.mark.parametrize('enable_audio_metadata_analysis', [True, False], indirect=True)
       def test_something():
           # Will run twice - once with analysis enabled, once disabled

    Args:
        request: The pytest request object containing the parametrized value if used with parametrize

    Yields:
        None: The fixture handles environment setup/teardown
    """

    # Get the enable value from parametrize or default to True
    enable = getattr(request, 'param', True)
    os.environ['AUDIO_META_ANALYSIS_ENABLED_OVERRIDE'] = str(enable).lower()
    yield
    os.environ['AUDIO_META_ANALYSIS_ENABLED_OVERRIDE'] = 'false'


def pytest_sessionfinish(session: Session, exitstatus: int) -> None:
    """
    Cleanup test user libraries after test run completion.

    This function is called after the entire test suite has finished executing.
    It performs cleanup operations by removing test user library directories
    to ensure a clean state for subsequent test runs.

    Args:
        session: The pytest Session object containing test run information
        exitstatus: The exit status code of the test run

    Returns:
        None
    """
    print("Executing post-test cleanup operations...")

    libraries_path = Path(settings.LIBRARIES_DIR)
    removed_dirs: List[str] = []
    failed_dirs: List[str] = []

    try:
        # Ensure the libraries directory exists
        if not libraries_path.exists():
            print(f"Warning: Libraries directory not found: {libraries_path}")
            return

        # Iterate through directory entries
        for entry in libraries_path.iterdir():
            print(f'Entry: {entry}')
            if entry.is_dir() and entry.name.startswith(settings.TEST_USER_LIBRARIES_DIR_NAME_PREFIXE):
                print(f"Removing test directory: {entry}")
                try:
                    shutil.rmtree(entry)
                    removed_dirs.append(str(entry))
                except (OSError, shutil.Error) as e:
                    failed_dirs.append(str(entry))
                    print(f"Error: Failed to remove directory {entry}: {str(e)}")
            else:
                print(f"Skipping non-test directory: {entry}")

        # Print summary
        if removed_dirs:
            print(f"\nSuccessfully removed {len(removed_dirs)} test directories:")
            for dir_path in removed_dirs:
                print(f"- {dir_path}")

        if failed_dirs:
            print(f"\nFailed to remove {len(failed_dirs)} test directories:")
            for dir_path in failed_dirs:
                print(f"- {dir_path}")

        print("Cleanup complete.")

    except Exception as e:
        print(f"Error: Unexpected error during cleanup: {str(e)}")
