"""Compatibility shim to re-expose audiometa_adapter at `api.utils.audiometa_adapter`.

Historically the module used to live under `api/utils/audiometa_adapter.py`.
It has been moved into the `audio_file_metadata` subpackage; tests and other code may still
import from the old path. This shim keeps the old import path working.
"""

# Re-export everything from the new module location
from .audio_file_metadata.audiometa_adapter import *  # noqa: F401,F403
from .audio_file_metadata.audiometa_adapter import _APP_TO_UNIFIED_KEY_MAP  # explicit export for tests
from .AppMetadataKey import AppMetadataKey  # explicit export for backward compatibility
from api.utils import get_file_path as _get_file_path  # alias for backward compatibility

# Re-export exceptions from package-level exceptions module if necessary
from .audio_file_metadata.exceptions import FileCorruptedError  # noqa: F401
