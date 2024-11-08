from django.db import models
from django.utils import timezone

from bodzify_api.model.base.BaseModel import BaseModel


class PublicStandardResource(BaseModel):
    created_on = models.DateTimeField(default=timezone.now, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=True)

    class Meta:
        abstract = True
