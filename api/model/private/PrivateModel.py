from django.db import models

from api import settings
from api.model.base.BaseModel import BaseModel


class PrivateModel(BaseModel):
    user = models.ForeignKey(f'{settings.APP_NAME}.User', on_delete=models.CASCADE, related_name='%(class)ss')

    class Meta:
        abstract = True
