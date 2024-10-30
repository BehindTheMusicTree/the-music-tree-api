
#!/usr/bin/env python

from django.db import models
from django.utils import timezone

from bodzify_api.model.base.utils.base_model.BaseModel import BaseModel


class Fields:
    CREATED_ON = 'created_on'
    UPDATED_ON = 'updated_on'


class PublicStandardResource(BaseModel):
    created_on = models.DateTimeField(default=timezone.now, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=True)

    class Meta:
        abstract = True
