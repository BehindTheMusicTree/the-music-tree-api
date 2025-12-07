from api.model.criteria.Criteria import Criteria
from api.model.criteria.type.CriteriaType import CriteriaType
from api.model.criteria.type.CriteriaTypePks import CriteriaTypePks

from .GenreManager import GenreManager


class Genre(Criteria):

    objects: 'GenreManager' = GenreManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.type = CriteriaType.objects.get(pk=CriteriaTypePks.GENRE)
        super().save(*args, **kwargs)
