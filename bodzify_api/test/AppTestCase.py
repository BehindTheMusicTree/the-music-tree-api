#!/usr/bin/env python

import inspect
import logging
import os
import shutil
from pathlib import Path
from typing import List
from django.http import HttpResponse, JsonResponse
from ddf import G
from rest_framework import status
from typing import Optional


from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken
from django.core.management import call_command

from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.File import File
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.track.LibraryTrack import LibraryTrack
import bodzify_api.settings as settings
from bodzify_api.test.AppApiClient import AppApiClient
from bodzify_api.test.ModelFixtureFactory import ModelFixtureFactory
from bodzify_api.test.TestUser import TestUser
from bodzify_api.view.viewset.model.AppModelViewSet import PAGINATED_RESPONSE_FIELDS


class AppTestCase(TestCase):
    TEST_USERNAME = "pytest_user"
    SAMPLE_DIR_NAME = "sample"
    LIB_SAMPLE_DIR_NAME = "library"
    INPUT_SAMPLE_DIR_NAME = "input"
    GENERIC_FILE_SAMPLE_PATH_RELATIVE_TO_TEST_DIR = Path("utils/generic_file_sample")

    api_client: AppApiClient

    @staticmethod
    def _merge_two_dicts(dict1, dict2):
        dict1.update(dict2)
        return dict1

    @staticmethod
    def _replace_none_values_by_empty_string(data_dict):
        if data_dict is None:
            return {}
        return {k: ('' if v is None else v) for k, v in data_dict.items()}

    def _set_up_test_directories_and_variables(self):
        specific_test_dir_abs_path = Path(os.path.dirname(inspect.getfile(self.__class__)))
        specific_test_sample_dir_abs_path = specific_test_dir_abs_path / self.SAMPLE_DIR_NAME
        self.lib_sample_dir_abs_path = specific_test_sample_dir_abs_path / self.LIB_SAMPLE_DIR_NAME
        self.specific_sample_dir_abs_path = specific_test_sample_dir_abs_path / self.INPUT_SAMPLE_DIR_NAME
        self.generic_sample_dir_abs_path = Path(os.path.dirname(os.path.abspath(__file__))) \
            / self.GENERIC_FILE_SAMPLE_PATH_RELATIVE_TO_TEST_DIR

    def _set_results_attributes(self, response):
        self.results = response.json()[PAGINATED_RESPONSE_FIELDS.RESULTS]
        self.overall_total = response.json()[PAGINATED_RESPONSE_FIELDS.OVERALL_TOTAL]

    def _set_result(self, response):
        self.result = response.json()

    def __login(self, user: User):
        self.api_client.force_authenticate(user=user)
        AccessToken.for_user(user)
        self.api_client.credentials(HTTP_AUTHORIZATION='Bearer {access}')

        response = self.api_client.get(path=reverse('playlist-list'), format='json')

        if response.status_code == status.HTTP_200_OK:
            assert True
        elif response.status_code == status.HTTP_401_UNAUTHORIZED:
            print("Not authenticated.")
            assert False
        else:
            print(f"Unexpected : {response.status_code}")
            assert False

    def setUp(self, methods_names_to_implement: Optional[list[str]] = None) -> None:
        call_command('loaddata', 'app', 'pytest_user')
        self.api_client = AppApiClient()
        self.test_user = TestUser(self.TEST_USERNAME)
        self._set_up_test_directories_and_variables()
        self.model_fixture_factory = ModelFixtureFactory(user=self.test_user.django_user,
                                                         lib_track_default_file_path=self.generic_sample_dir_abs_path /
                                                         '.mp3')
        if os.path.isdir(self.lib_sample_dir_abs_path):
            for file_relative_path in os.listdir(self.lib_sample_dir_abs_path):
                self.test_user.copy_file_to_lib(self.lib_sample_dir_abs_path / file_relative_path)
        self.__login(self.test_user.django_user)

        super().setUp()

        if methods_names_to_implement is not None:
            for method_name in methods_names_to_implement:
                if not hasattr(self, method_name) or not callable(getattr(self, method_name)):
                    raise NotImplementedError(f"Subclasses must implement the '{method_name}' method")
