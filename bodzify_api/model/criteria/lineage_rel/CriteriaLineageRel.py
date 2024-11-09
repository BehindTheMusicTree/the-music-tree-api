from django.db import models

from bodzify_api.model.private_standard_resource.PrivateStandardResource import PrivateStandardResource
from ..Fields import Fields as CriteriaFields
from ..Criteria import Criteria
from .Fields import Fields


class CriteriaLineageRel(PrivateStandardResource):
    descendant = models.ForeignKey(Criteria, on_delete=models.CASCADE, related_name=CriteriaFields.ASCENDANTS_RELS)
    ascendant = models.ForeignKey(Criteria, on_delete=models.CASCADE, related_name=CriteriaFields.DESCENDANTS_RELS)
    degree = models.PositiveIntegerField()

    def __str__(self):
        return f'Descendant {self.descendant.uuid} | Degree {self.degree} | Ascendant {self.ascendant.uuid}'

    class Meta:
        verbose_name = 'Criteria Lineage Relation'
        verbose_name_plural = 'Criteria Lineage Relations'
        indexes = [models.Index(fields=[Fields.USER], name='crit_lineage_rel_user_idx')]
