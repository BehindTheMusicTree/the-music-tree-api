#!/usr/bin/env python

from pathlib import Path
import bodzify_api.settings as settings

MEDIA_TEMP = Path(settings.MEDIA_ROOT) / "temp"
LIBRARIES_DIR_NAME = "libraries"
LIBRARIES_PATH = Path(settings.MEDIA_ROOT) / LIBRARIES_DIR_NAME
