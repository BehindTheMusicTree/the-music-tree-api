from django.apps import AppConfig

from app import settings


class BodzifyApiConfig(AppConfig):
    name = settings.APP_NAME
