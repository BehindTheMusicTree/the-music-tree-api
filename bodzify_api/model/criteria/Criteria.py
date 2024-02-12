#!/usr/bin/env python

import logging
from typing import Optional
import shortuuid
from django.db import models
from django.contrib.auth.models import User
import bodzify_api.settings as settings

logger = logging.getLogger('bodzify_api')

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
    
    def get_new_root_value_updating_in_kwargs(self, kwargs):
        return kwargs.get(ATTRIBUTES_LABEL.ROOT, self.root)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        is_root_uptating = ATTRIBUTES_LABEL.ROOT in kwargs.get("update_fields", [])
        if not is_root_uptating:
            is_creation = not self.root
            if is_creation:
                if self.parent:
                    self.root = self.parent.root
                else:
                    self.root = self
                self.save(update_fields=[ATTRIBUTES_LABEL.ROOT])
            else:
                new_root = self.parent.root if self.parent else self
                if self.root != new_root:
                    self._update_root_of_criteria_and_children(self, new_root) # type: ignore

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
        return self.is_criteria1_descendant_of_criteria2(self, other_criteria)
    
    def is_criteria1_descendant_of_criteria2(self, criteria1: 'Criteria', criteria2: 'Criteria'):
        if criteria1.parent == criteria2:
            return True
        elif criteria1.parent:
            return self.is_criteria1_descendant_of_criteria2(criteria1.parent, criteria2)
        else:
            return False
    
    def get_children(self):
        return Criteria.objects.filter(parent=self)
    
    def _update_root_of_criteria_and_children(self, criteria: 'Criteria', new_root: 'Criteria'):
        criteria.root = new_root # type: ignore
        criteria.save(update_fields=[ATTRIBUTES_LABEL.ROOT])
        children = criteria.get_children()
        if children.exists():
            for child in children:
                self._update_root_of_criteria_and_children(child, new_root)
    
    def _update_root_of_descandants_if_root_different(self, 
                                                      old_criteria_root: Optional['Criteria'], 
                                                      saved_criteria: 'Criteria'):
        if old_criteria_root != saved_criteria.root:
            self._update_root_of_criteria_and_children(
                criteria=saved_criteria, 
                new_root=saved_criteria.root) # type: ignore