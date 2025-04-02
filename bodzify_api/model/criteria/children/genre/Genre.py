from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.type.CriteriaType import CriteriaType
from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypePks

from .GenreManager import GenreManager


class Genre(Criteria):

    objects: 'GenreManager' = GenreManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.type = CriteriaType.objects.get(pk=CriteriaTypePks.GENRE)
        super().save(*args, **kwargs)