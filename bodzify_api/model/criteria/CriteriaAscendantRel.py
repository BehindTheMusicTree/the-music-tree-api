#!/usr/bin/env python

from django.db import models

from bodzify_api.model.base.PrivateStandardResource import PrivateStandardResource, Fields as PrivateRelationFields
from bodzify_api.model.criteria.Criteria import Fields as ModelFields, Criteria


class Fields:
    MODEL = "criteria_ascendant_relation"
    CREATED_ON = PrivateRelationFields.CREATED_ON
    UPDATED_ON = PrivateRelationFields.UPDATED_ON
    USER = PrivateRelationFields.USER
    DESCENDANT = 'descendant'
    ASCENDANT = 'ascendant'
    DEGREE = "degree"
    ADDED_ON = "added_on"


class CriteriaAscendantRel(PrivateStandardResource):
    descendant = models.ForeignKey(Criteria,
                                   on_delete=models.CASCADE,
                                   related_name=ModelFields.CRITERIA_ASCENDANT_RELATION_ASCENDANTS)
    ascendant = models.ForeignKey(Criteria,
                                  on_delete=models.CASCADE,
                                  related_name=ModelFields.CRITERIA_ASCENDANT_RELATION_DESCENDANTS)
    degree = models.PositiveIntegerField()
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Descendant {self.descendant.uuid} - Degree {self.degree} Ascendant {self.ascendant.uuid}'

    class Meta:
        db_table = 'bodzify_api_criteria_ascendant_rel'
        indexes = [models.Index(fields=[Fields.USER], name='criteria_asc_rel_user_idx')]
