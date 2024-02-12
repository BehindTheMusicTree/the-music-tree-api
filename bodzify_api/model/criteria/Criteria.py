#!/usr/bin/env python
from collections.abc import Iterable
import shortuuid
from django.db import models
from django.contrib.auth.models import User
import bodzify_api.settings as settings

class SPECIAL_NAMES:
    ALL = "All"

class ATTRIBUTES_LABEL:
    UUID = "uuid"
    USER = "user"
    NAME = "name"
    TYPE = "type"
    PARENT = "parent"
    CHILDREN = "children"
    ROOT = "root"
    ADDED_ON = "addedOn"

class Criteria(models.Model):
    uuid = models.CharField(
        primary_key=True, default=shortuuid.uuid, max_length=22, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(
        max_length=settings.CRITERIA_NAME_MAX_CHAR, default=None)
    type = models.ForeignKey('bodzify_api.CriteriaType',
                             on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='child_criteria')
    root = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='descendant_criteria')
    addedOn = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        unique_together = (ATTRIBUTES_LABEL.USER, ATTRIBUTES_LABEL.NAME)
        constraints = [
            models.CheckConstraint(check=~models.Q(
                name=""), name="criteria_non_empty_name")
        ]

    def __str__(self) -> str:
        return self.uuid + " " + self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.root is None:
            self.root = self
            self.save(update_fields=[ATTRIBUTES_LABEL.ROOT])

    def get_common_criteria(self, criteriaB):
        visited = set()

        criteriaATreeItem = self
        while criteriaATreeItem is not None:
            visited.add(criteriaATreeItem)
            criteriaATreeItem = criteriaATreeItem.parent

        criteriaBTreeItem = criteriaB
        while criteriaBTreeItem is not None:
            if criteriaBTreeItem in visited:
                return criteriaBTreeItem
            criteriaBTreeItem = criteriaBTreeItem.parent

        return None

    def is_descendant_of(self, other_criteria):
        current_criteria = self
        while current_criteria:
            if current_criteria == other_criteria:
                return True
            current_criteria = current_criteria.parent
        return False
    
    def get_children(self):
        return Criteria.objects.filter(parent=self)