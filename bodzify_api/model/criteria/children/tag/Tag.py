from django.db import models

from bodzify_api import settings
from ...Criteria import Criteria
from ....criteria_acendant_rel.Fields import Fields as CriteriaAscendantRelFields
from .Fields import Fields


class Tag(Criteria):

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name=Fields.CHILD)
    ascendants = models.ManyToManyField('self', through='TagAscendantRel',
                                        through_fields=(CriteriaAscendantRelFields.DESCENDANT,
                                                        CriteriaAscendantRelFields.ASCENDANT),
                                        related_name=Fields.DESCENDANTS,
                                        symmetrical=False)

    class Meta(Criteria.Meta):
        db_table = f'{settings.APP_NAME}_tag'
