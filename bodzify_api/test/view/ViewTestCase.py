import magic
import os
import shutil

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from django.test import TestCase
from django.contrib.auth.models import User

import bodzify_api.settings as settings

TEST_USERNAME = "test_django"

class ViewTestCase(TestCase):

    def setUpTestUserDirectories(self):
        testUserLibraryAbsolutePath = (
            settings.LIBRARIES_PATH 
            + settings.USER_LIBRARY_FOLDER_NAME_PREFIXE 
            + str(self.testUser.pk))
        if not os.path.exists(testUserLibraryAbsolutePath):
            os.makedirs(testUserLibraryAbsolutePath)
        self.sampleDirectoryAbsolutePath = settings.APP_ROOT + self.sampleDirectoryRelativePath
        self.testUserLibraryRelativePath = (
            settings.LIBRARIES_FOLDER_NAME
            + "/" + settings.USER_LIBRARY_FOLDER_NAME_PREFIXE 
            + str(self.testUser.pk) + "/")
        self.testUserLibraryAbsolutePath = settings.MEDIA_ROOT +  self.testUserLibraryRelativePath
        self.emptyUserLibrary()

    def setUp(self, sampleRelativePath="") -> None:

        self.sampleDirectoryRelativePath = sampleRelativePath
        self.mime = magic.Magic(mime=True)
        self.apiClient = APIClient()
        self.testUser = User.objects.get(username=TEST_USERNAME)
        self.setUpTestUserDirectories()
        return super().setUp()

    def login(self, user):
        self.apiClient.force_authenticate(user=user)
        access = AccessToken.for_user(user)
        self.apiClient.credentials(HTTP_AUTHORIZATION='Bearer {access}')
    
    def emptyUserLibrary(self):
        for filename in os.listdir(self.testUserLibraryAbsolutePath):
            filePath = os.path.join(self.testUserLibraryAbsolutePath, filename)
            try:
                if os.path.isfile(filePath) or os.path.islink(filePath):
                    os.unlink(filePath)
                elif os.path.isdir(filePath):
                    shutil.rmtree(filePath)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (filePath, e))
    
    def copySamplesToTestUserLibrary(self):            
        fileNames = os.listdir(self.sampleDirectoryAbsolutePath)
        for fileName in fileNames:
            shutil.copy(
                os.path.join(self.sampleDirectoryAbsolutePath, fileName),
                self.testUserLibraryAbsolutePath)
