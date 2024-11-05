from django.apps import AppConfig

from bodzify_api import settings


class BodzifyApiConfig(AppConfig):
    name = settings.APP_NAME
