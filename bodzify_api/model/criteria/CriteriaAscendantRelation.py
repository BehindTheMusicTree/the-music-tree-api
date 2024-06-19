#!/usr/bin/env python

from django.db import models

from bodzify_api.model.criteria.Criteria import Criteria, ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL


class ATTRIBUTES_LABEL:
    MODEL = "criteria_ascendant_relation"
    DESCENDANT = "descendant"
    ASCENDANT = "ascendant"
    DEGREE = "degree"
    ADDED_ON = "added_on"


class CriteriaAscendantRelation(models.Model):
    descendant = models.ForeignKey(Criteria,
                                   on_delete=models.CASCADE,
                                   related_name=CRITERIA_ATTRIBUTES_LABEL.CRITERIA_ASCENDANT_RELATION_ASCENDANTS)
    ascendant = models.ForeignKey(Criteria,
                                  on_delete=models.CASCADE,
                                  related_name=CRITERIA_ATTRIBUTES_LABEL.CRITERIA_ASCENDANT_RELATION_DESCENDANTS)
    degree = models.PositiveIntegerField()
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Descendant {self.descendant.uuid} - Degree {self.degree} Ascendant {self.ascendant.uuid}'

    class Meta:
        db_table = 'bodzify_api_criteria_ascendant_relation'
