from django.db import models

from ..base.PrivateStandardResource import PrivateStandardResource
from ..criteria.Criteria import Criteria
from .Fields import Fields as ModelFields


class CriteriaAscendantRel(PrivateStandardResource):
    descendant = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    ascendant = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    degree = models.PositiveIntegerField()
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Descendant {self.descendant.uuid} | Degree {self.degree} | Ascendant {self.ascendant.uuid}'

    class Meta:
        abstract = True
        indexes = [models.Index(fields=[ModelFields.USER], name='%(class)s_asc_rel_user_idx')]
