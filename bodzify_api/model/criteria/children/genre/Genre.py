from django.db import models

from bodzify_api import settings
from ....criteria_acendant_rel.Fields import Fields as CriteriaAscendantRelFields
from ...Criteria import Criteria
from .Fields import Fields


class Genre(Criteria):

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name=Fields.CHILD)
    ascendants = models.ManyToManyField('self', through='GenreAscendantRel',
                                        through_fields=(CriteriaAscendantRelFields.DESCENDANT,
                                                        CriteriaAscendantRelFields.ASCENDANT),
                                        related_name=Fields.DESCENDANTS,
                                        symmetrical=False)

    class Meta(Criteria.Meta):
        db_table = f'{settings.APP_NAME}_genre'
