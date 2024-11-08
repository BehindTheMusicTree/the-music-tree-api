import uuid

from django.db import models

from bodzify_api.model.base.BaseModel import BaseModel


class UuidModel(BaseModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True
