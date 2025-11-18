import os
import shutil
from pathlib import Path

import pytest
from _pytest.main import Session
from django.test import override_settings
from bodzify_api import settings


@pytest.fixture(autouse=True)
def set_debug_for_tests():
    """Set DEBUG=True by default for tests.

    Individual tests can use @override_settings(DEBUG=False) when needed.
    """
    with override_settings(DEBUG=True):
        yield


critical_test_failed = False


IGNORED_TEST_DIRS = [
    'utils/',
]


def pytest_ignore_collect(path, config):
    str_path = str(path)
    return any(ignored_dir in str_path for ignored_dir in IGNORED_TEST_DIRS)


def base_childinstance(request, db):
    test_case = request.param()
    test_case.setUp()
    yield test_case
    test_case.tearDown


def pytest_configure(config):
    config.addinivalue_line("markers", "critical: mark test as critical to pass")
    config.addinivalue_line("markers", "slow: mark test as long-running")


def pytest_runtest_makereport(item, call):
    global critical_test_failed
    critical_marker = item.get_closest_marker("critical")
    if call.when == "call" and critical_marker:
        if call.excinfo:
            critical_test_failed = True
            print(f"\nCRITICAL TEST FAILED: {item.name}")
            print(f"Output: {call.excinfo}")


def _check_disk_space(min_free_gb: float = 0.5) -> bool:
    """Check if there's enough disk space available.
    
    Args:
        min_free_gb: Minimum free space required in GB (default: 0.5GB)
        
    Returns:
        True if enough space is available, False otherwise
    """
    try:
        stat = shutil.disk_usage(settings.LIBRARIES_DIR)
        free_gb = stat.free / (1024**3)
        return free_gb >= min_free_gb
    except Exception:
        return True


def _test_requires_file_operations(item) -> bool:
    """Check if a test requires file operations based on its path.
    
    Args:
        item: The pytest test item
        
    Returns:
        True if the test likely requires file operations
    """
    test_path = str(item.fspath)
    file_operation_paths = [
        'uploaded_track',
        'test_lib_tracks',
    ]
    return any(path in test_path for path in file_operation_paths)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    if critical_test_failed:
        pytest.skip("A critical test has failed. Skipping the rest of the tests..")
    
    if _test_requires_file_operations(item) and not _check_disk_space():
        try:
            stat = shutil.disk_usage(settings.LIBRARIES_DIR)
            free_gb = stat.free / (1024**3)
            pytest.skip(
                f"Insufficient disk space. Free space: {free_gb:.2f}GB. "
                f"Tests requiring file operations are skipped when free space is below 0.5GB. "
                f"Please free up disk space to run these tests."
            )
        except Exception:
            pass


def pytest_collection_modifyitems(config, items):
    # Set critical tests first and slow tests last
    critical_tests = []
    normal_tests = []
    slow_tests = []

    print("Ordering tests: critical tests first, slow tests last")
    for item in items:
        critical_marker = item.get_closest_marker("critical")
        slow_marker = item.get_closest_marker("slow")

        if critical_marker:
            critical_tests.append(item)
        elif slow_marker:
            slow_tests.append(item)
        else:
            normal_tests.append(item)

    items[:] = critical_tests + normal_tests + slow_tests


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


def _cleanup_test_user_directories() -> None:
    """Cleanup test user library directories.
    
    This function removes all test user library directories that start with
    TEST_USER_LIBRARIES_DIR_NAME_PREFIXE. It's called from multiple hooks to ensure
    cleanup happens even if tests are interrupted or fail.
    """
    libraries_path = Path(settings.LIBRARIES_DIR)
    removed_dirs: list[str] = []
    failed_dirs: list[str] = []

    try:
        if not libraries_path.exists():
            return

        for entry in libraries_path.iterdir():
            if entry.is_dir() and entry.name.startswith(settings.TEST_USER_LIBRARIES_DIR_NAME_PREFIXE):
                try:
                    shutil.rmtree(entry)
                    removed_dirs.append(str(entry))
                except (OSError, shutil.Error) as e:
                    failed_dirs.append(str(entry))
                    print(f"Error: Failed to remove directory {entry}: {str(e)}")

        if removed_dirs:
            print(f"\nSuccessfully removed {len(removed_dirs)} test directories:")
            for dir_path in removed_dirs:
                print(f"- {dir_path}")

        if failed_dirs:
            print(f"\nFailed to remove {len(failed_dirs)} test directories:")
            for dir_path in failed_dirs:
                print(f"- {dir_path}")

    except Exception as e:
        print(f"Error: Unexpected error during cleanup: {str(e)}")


@pytest.hookimpl(trylast=True)
def pytest_runtest_teardown(item, nextitem):
    """Cleanup test user directories after each test if it's the last test in the class."""
    if nextitem is None or nextitem.cls != item.cls:
        _cleanup_test_user_directories()


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
    _cleanup_test_user_directories()
    print("Cleanup complete.")


@pytest.hookimpl(trylast=True)
def pytest_unconfigure(config):
    """Cleanup test user directories when pytest is unconfigured (e.g., on interruption)."""
    _cleanup_test_user_directories()
