from api.model.criteria.Criteria import Criteria
from api.model.criteria.type.CriteriaType import CriteriaType
from api.model.criteria.type.CriteriaTypePks import CriteriaTypePks
from .TagManager import TagManager


class Tag(Criteria):

    objects: 'TagManager' = TagManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.type = CriteriaType.objects.get(pk=CriteriaTypePks.TAG)
        super().save(*args, **kwargs)
