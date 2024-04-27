#!/usr/bin/env python

import os
from pathlib import Path
import shutil
from typing import Any, List
from django.contrib.auth.models import User

from bodzify_api import settings


class TestUser():
    lib_abs_path: Path
    lib_path_relative_to_media_dir: Path
    django_user: User

    def __empty_user_library(self):
        for filename in os.listdir(self.lib_abs_path):
            filePath = os.path.join(self.lib_abs_path, filename)
            try:
                if os.path.isfile(filePath) or os.path.islink(filePath):
                    os.unlink(filePath)
                elif os.path.isdir(filePath):
                    shutil.rmtree(filePath)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (filePath, e))

    def __set_up_dirs(self):
        self.lib_abs_path = settings.LIB_PATH / Path(settings.USER_LIB_DIR_NAME_PREFIXE + str(self.django_user.pk))
        if not self.lib_abs_path.exists():
            os.makedirs(self.lib_abs_path)

        self.lib_path_relative_to_media_dir = \
            Path(settings.LIB_DIR_NAME) / (settings.USER_LIB_DIR_NAME_PREFIXE + str(self.django_user.pk))
        self.lib_abs_path = settings.MEDIA_ROOT / self.lib_path_relative_to_media_dir
        self.__empty_user_library()

    def __init__(self, username: str) -> None:
        self.django_user = User.objects.get(username=username)
        self.__set_up_dirs()

    def copy_file_to_lib(self, files_abs_path: Path):
        shutil.copy(files_abs_path, self.lib_abs_path)

    def does_track_filename_exist_in_lib(self, filename: str):
        return os.path.isfile(self.lib_abs_path / filename)
