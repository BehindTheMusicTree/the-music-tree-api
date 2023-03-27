#!/usr/bin/env python
import shortuuid
from django.db import models
from django.contrib.auth.models import User


class CriteriaSpecialNames:
    GENRE_ALL = "All"
    GENRE_GENRELESS = "Genreless"
    TAG_ALL = "Tagged"


class Criteria(models.Model):
    uuid = models.CharField(
        primary_key=True, default=shortuuid.uuid, max_length=22, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=200, default=None)
    type = models.ForeignKey('bodzify_api.CriteriaType', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    addedOn = models.DateTimeField(auto_now_add=True, editable=False)
    

    class Meta:
        unique_together = ('user', 'name')


    def __str__(self) -> str:
        return self.uuid + " " + self.name


    def getCommonCriteria(self, criteriaB):
        criteriaATreeItem = self
        while True:
            criteriaBTreeItem = criteriaB
            while criteriaBTreeItem is not None:
                if criteriaATreeItem == criteriaBTreeItem:
                    return criteriaBTreeItem
                else:
                    criteriaBTreeItem = criteriaBTreeItem.parent
            criteriaATreeItem = criteriaATreeItem.parent

