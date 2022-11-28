#!/usr/bin/env python

import shortuuid

from django.db import models
from django.contrib.auth.models import User

from bodzify_api.model.criteria.CriteriaType import CriteriaType

class Criteria(models.Model):
    uuid = models.CharField(primary_key=True, default=shortuuid.uuid, max_length=200, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    type = models.ForeignKey(CriteriaType, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, default=None, blank=True, null=True)
    addedOn = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.uuid + " " + self.name + " " + str(self.parent)

    class Meta:
        unique_together = ('user', 'name', 'type')