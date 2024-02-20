#!/usr/bin/env python
import inspect
import os
import logging
from pathlib import Path
import shutil
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from django.test import TestCase
from django.contrib.auth.models import User
import bodzify_api.settings as settings

TEST_USERNAME = "pytest_user"
SAMPLE_DIR_NAME = "sample"
LIBRARY_SAMPLE_DIR_NAME = "library"
INPUT_SAMPLE_DIR_NAME = "input"

logger = logging.getLogger('bodzify_api')

class ViewTestCase(TestCase):

    fixtures = ['app_initial_data', 'pytest_user_initial_data']
    test_user_library_path_relative_to_media_dir = Path()

    def setUp(self) -> None:
        self.api_client = APIClient()
        self.test_user = User.objects.get(username=TEST_USERNAME)
        self._set_up_test_user_directories()
        if os.path.isdir(self.library_sample_dir_abs_path):
            self._copyLibrarySamplesToTestUserLibrary()
        self._login(self.test_user)
        return super().setUp()

    def _set_up_test_user_directories(self):
        test_user_library_abs_path = settings.LIBRARIES_PATH / \
                                  (settings.USER_LIBRARY_DIR_NAME_PREFIXE + \
                                  str(self.test_user.pk))
        if not test_user_library_abs_path.exists():
            os.makedirs(test_user_library_abs_path)

        test_dir_abs_path = Path(os.path.dirname(inspect.getfile(self.__class__)))
        sample_dir_abs_path = test_dir_abs_path / SAMPLE_DIR_NAME
        self.library_sample_dir_abs_path = sample_dir_abs_path / LIBRARY_SAMPLE_DIR_NAME
        self.input_sample_dir_abs_path = sample_dir_abs_path / INPUT_SAMPLE_DIR_NAME

        self.test_user_library_path_relative_to_media_dir = \
            Path(settings.LIBRARIES_DIR_NAME) / \
            (settings.USER_LIBRARY_DIR_NAME_PREFIXE + str(self.test_user.pk))
        self.test_user_library_abs_path = settings.MEDIA_ROOT / \
            self.test_user_library_path_relative_to_media_dir
        self._empty_user_library()

    def _login(self, user):
        self.api_client.force_authenticate(user=user)
        AccessToken.for_user(user)
        self.api_client.credentials(HTTP_AUTHORIZATION='Bearer {access}')

    def _empty_user_library(self):
        for filename in os.listdir(self.test_user_library_abs_path):
            filePath = os.path.join(self.test_user_library_abs_path, filename)
            try:
                if os.path.isfile(filePath) or os.path.islink(filePath):
                    os.unlink(filePath)
                elif os.path.isdir(filePath):
                    shutil.rmtree(filePath)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (filePath, e))

    def _copyLibrarySamplesToTestUserLibrary(self):
        filenames = os.listdir(self.library_sample_dir_abs_path)
        for filename in filenames:
            shutil.copy(self.library_sample_dir_abs_path / filename,
                self.test_user_library_abs_path)

    def does_track_filename_exist_in_test_user_library(self, filename: str):
        return os.path.isfile(self.test_user_library_abs_path / filename)
