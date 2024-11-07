from django.db import models

from bodzify_api import settings
from bodzify_api.model.base.PrivateStandardResource import PrivateStandardResource
from ..Criteria import Criteria
from ..Fields import Fields as CriteriaFields
from .Fields import Fields


class CriteriaLineageRel(PrivateStandardResource):
    descendant = models.ForeignKey(Criteria, on_delete=models.CASCADE, related_name=CriteriaFields.ASCENDANTS_REL)
    ascendant = models.ForeignKey(Criteria, on_delete=models.CASCADE, related_name=CriteriaFields.DESCENDANTS_REL)
    degree = models.PositiveIntegerField()

    def __str__(self):
        return f'Descendant {self.descendant.uuid} | Degree {self.degree} | Ascendant {self.ascendant.uuid}'

    class Meta:
        db_table = f'{settings.APP_NAME}_criteria_lineage_rel'
        verbose_name = 'Criteria Lineage Relation'
        verbose_name_plural = 'Criteria Lineage Relations'
        indexes = [models.Index(fields=[Fields.USER], name='crit_lineage_rel_user_idx')]
