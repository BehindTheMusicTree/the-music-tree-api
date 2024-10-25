
#!/usr/bin/env python

from django.db import models
from django.utils import timezone


class Fields:
    CREATED_ON = 'created_on'
    UPDATED_ON = 'updated_on'


class PublicStandardResource(models.Model):
    created_on = models.DateTimeField(default=timezone.now, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=True)

    class Meta:
        abstract = True
