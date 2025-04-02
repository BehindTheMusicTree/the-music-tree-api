from django.db import models

from bodzify_api import settings
from bodzify_api.model.base.BaseModel import BaseModel


class PrivateModel(BaseModel):
    user = models.ForeignKey(f'{settings.APP_NAME}.User', on_delete=models.CASCADE, related_name='%(class)ss')

    class Meta:
        abstract = True
