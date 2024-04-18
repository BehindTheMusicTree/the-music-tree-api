#!/usr/bin/env python

import inspect
import logging
import os
import shutil
from pathlib import Path
from rest_framework import status

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from django.core.management import call_command

import bodzify_api.settings as settings


logger = logging.getLogger('bodzify_api')


class AppTestCase(TestCase):

    TEST_USERNAME = "pytest_user"
    SAMPLE_DIR_NAME = "sample"
    LIB_SAMPLE_DIR_NAME = "library"
    INPUT_SAMPLE_DIR_NAME = "input"
    GENERIC_FILE_SAMPLE_PATH_RELATIVE_TO_TEST_DIR = Path("utils/generic_file_sample")

    test_user_lib_path_relative_to_media_dir = Path()

    def setUp(self) -> None:
        call_command('loaddata', 'app', 'pytest_user')
        self.api_client = APIClient()
        self.test_user = User.objects.get(username=self.TEST_USERNAME)
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
            Path(os.path.dirname(os.path.abspath(__file__))) / self.GENERIC_FILE_SAMPLE_PATH_RELATIVE_TO_TEST_DIR

        specific_test_dir_abs_path = Path(os.path.dirname(inspect.getfile(self.__class__)))
        specific_test_sample_dir_abs_path = specific_test_dir_abs_path / self.SAMPLE_DIR_NAME
        self.lib_sample_dir_abs_path = specific_test_sample_dir_abs_path / self.LIB_SAMPLE_DIR_NAME
        self.specific_sample_dir_abs_path = specific_test_sample_dir_abs_path / self.INPUT_SAMPLE_DIR_NAME

        self.test_user_lib_path_relative_to_media_dir = \
            Path(settings.LIB_DIR_NAME) / (settings.USER_LIB_DIR_NAME_PREFIXE + str(self.test_user.pk))
        self.test_user_lib_abs_path = settings.MEDIA_ROOT / self.test_user_lib_path_relative_to_media_dir
        self.__empty_user_library()

    def __login(self, user):
        self.api_client.force_authenticate(user=user)
        AccessToken.for_user(user)
        self.api_client.credentials(HTTP_AUTHORIZATION='Bearer {access}')

        response = self.api_client.get(path=reverse('playlist-list'), format='json')

        if response.status_code == status.HTTP_200_OK:  # type: ignore
            assert True
        elif response.status_code == status.HTTP_401_UNAUTHORIZED:  # type: ignore
            print("Not authenticated.")
            assert False
        else:
            print(f"Unexpected : {response.status_code}")  # type: ignore
            assert False

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
