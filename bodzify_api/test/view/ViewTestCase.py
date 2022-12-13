import magic

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
import bodzify_api.settings as settings

TEST_USER_PK = 2

class ViewTestCase(TestCase):

    fixtures = ['initial_data', 'test_data']

    def setUp(self, sampleRelativePath) -> None:
        self.sampleRelativePath = sampleRelativePath
        self.mime = magic.Magic(mime=True)
        self.apiClient = APIClient()
        self.testUser = User.objects.get(pk=TEST_USER_PK)
        self.sampleAbsolutePath = settings.APP_ROOT + self.sampleRelativePath
        return super().setUp()

    def login(self, user):
        self.apiClient.force_authenticate(user=user)
        access = AccessToken.for_user(user)
        self.apiClient.credentials(HTTP_AUTHORIZATION='Bearer {access}')
