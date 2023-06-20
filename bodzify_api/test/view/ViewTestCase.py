#!/usr/bin/env python
import inspect
import os
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


class ViewTestCase(TestCase):

    fixtures = ['app_initial_data', 'pytest_user_initial_data']
    testUserLibraryPathRelativeToMediaDir = ""

    def setUp(self) -> None:
        self.apiClient = APIClient()
        self.testUser = User.objects.get(username=TEST_USERNAME)
        self._setUpTestUserDirectories()
        if os.path.isdir(self.librarySampleDirAbsPath):
            self._copyLibrarySamplesToTestUserLibrary()
        self._login(self.testUser)
        return super().setUp()

    def _setUpTestUserDirectories(self):
        testUserLibraryAbsPath = (
            settings.LIBRARIES_PATH
            + settings.USER_LIBRARY_DIR_NAME_PREFIXE
            + str(self.testUser.pk))
        if not os.path.exists(testUserLibraryAbsPath):
            os.makedirs(testUserLibraryAbsPath)

        testDirAbsPathWithoutSlash = os.path.dirname(
            inspect.getfile(self.__class__))
        sampleDirAbsPath = testDirAbsPathWithoutSlash + "/" + SAMPLE_DIR_NAME + "/"
        self.librarySampleDirAbsPath = sampleDirAbsPath + "/" + LIBRARY_SAMPLE_DIR_NAME + "/"
        self.inputSampleDirAbsPath = sampleDirAbsPath + "/" + INPUT_SAMPLE_DIR_NAME + "/"

        self.testUserLibraryPathRelativeToMediaDir = (
            settings.LIBRARIES_DIR_NAME + "/"
            + settings.USER_LIBRARY_DIR_NAME_PREFIXE
            + str(self.testUser.pk)
            + "/")
        self.testUserLibraryAbsPath = settings.MEDIA_ROOT \
            + self.testUserLibraryPathRelativeToMediaDir
        self._emptyUserLibrary()

    def _login(self, user):
        self.apiClient.force_authenticate(user=user)
        access = AccessToken.for_user(user)
        self.apiClient.credentials(HTTP_AUTHORIZATION='Bearer {access}')

    def _emptyUserLibrary(self):
        for filename in os.listdir(self.testUserLibraryAbsPath):
            filePath = os.path.join(self.testUserLibraryAbsPath, filename)
            try:
                if os.path.isfile(filePath) or os.path.islink(filePath):
                    os.unlink(filePath)
                elif os.path.isdir(filePath):
                    shutil.rmtree(filePath)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (filePath, e))

    def _copyLibrarySamplesToTestUserLibrary(self):
        filenames = os.listdir(self.librarySampleDirAbsPath)
        for filename in filenames:
            shutil.copy(
                os.path.join(self.librarySampleDirAbsPath, filename),
                self.testUserLibraryAbsPath)

    def doesTrackFilenameExistInTestUserLibrary(self, filename: str):
        return os.path.isfile(self.testUserLibraryAbsPath + filename)
