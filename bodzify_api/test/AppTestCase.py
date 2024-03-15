#!/usr/bin/env python

import inspect
import logging
import os
import shutil
from pathlib import Path

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from django.core.management import call_command

import bodzify_api.settings as settings

TEST_USERNAME = "pytest_user"
SAMPLE_DIR_NAME = "sample"
LIB_SAMPLE_DIR_NAME = "library"
INPUT_SAMPLE_DIR_NAME = "input"
GENERIC_FILE_SAMPLE_DIR_NAME = "generic_file_sample"


logger = logging.getLogger('bodzify_api')


class AppTestCase(TestCase):

    class LIB_TRACK_GENERIC_SAMPLES_FILENAMES_WITHOUT_EXTENSION:
        ONE_STAR = "1 star"
        TAGS_NONE = "tags none"
        TAGS_ALBUM_WITHOUT_ALBUM_ARTISTS = "tags album without album artists"
        TAGS_MAX_LENGTH_WITH_LETTER_A = "tags max length with letter a"

    test_user_lib_path_relative_to_media_dir = Path()

    def setUp(self) -> None:
        call_command('loaddata', 'app_initial_data', 'pytest_user_initial_data')
        self.api_client = APIClient()
        self.test_user = User.objects.get(username=TEST_USERNAME)
        self.__set_up_test_user_directories()
        if os.path.isdir(self.lib_sample_dir_abs_path):
            self.__copy_lib_samples_to_test_user_lib()
        self.__login(self.test_user)
        return super().setUp()

    def __set_up_test_user_directories(self):
        test_user_lib_abs_path = settings.LIB_PATH / Path(settings.USER_LIB_DIR_NAME_PREFIXE + str(self.test_user.pk))
        if not test_user_lib_abs_path.exists():
            os.makedirs(test_user_lib_abs_path)

        self.generic_sample_dir_abs_path = \
            Path(os.path.dirname(os.path.abspath(__file__))) / GENERIC_FILE_SAMPLE_DIR_NAME

        specific_test_dir_abs_path = Path(os.path.dirname(inspect.getfile(self.__class__)))
        specific_test_sample_dir_abs_path = specific_test_dir_abs_path / SAMPLE_DIR_NAME
        self.lib_sample_dir_abs_path = specific_test_sample_dir_abs_path / LIB_SAMPLE_DIR_NAME
        self.specific_sample_dir_abs_path = specific_test_sample_dir_abs_path / INPUT_SAMPLE_DIR_NAME

        self.test_user_lib_path_relative_to_media_dir = \
            Path(settings.LIB_DIR_NAME) / (settings.USER_LIB_DIR_NAME_PREFIXE + str(self.test_user.pk))
        self.test_user_lib_abs_path = settings.MEDIA_ROOT / self.test_user_lib_path_relative_to_media_dir
        self.__empty_user_library()

    def __login(self, user):
        self.api_client.force_authenticate(user=user)
        AccessToken.for_user(user)
        self.api_client.credentials(HTTP_AUTHORIZATION='Bearer {access}')

    def __empty_user_library(self):
        for filename in os.listdir(self.test_user_lib_abs_path):
            filePath = os.path.join(self.test_user_lib_abs_path, filename)
            try:
                if os.path.isfile(filePath) or os.path.islink(filePath):
                    os.unlink(filePath)
                elif os.path.isdir(filePath):
                    shutil.rmtree(filePath)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (filePath, e))

    def __copy_lib_samples_to_test_user_lib(self):
        filenames = os.listdir(self.lib_sample_dir_abs_path)
        for filename in filenames:
            shutil.copy(self.lib_sample_dir_abs_path / filename,
                        self.test_user_lib_abs_path)

    def _does_track_filename_exist_in_test_user_lib(self, filename: str):
        return os.path.isfile(self.test_user_lib_abs_path / filename)
