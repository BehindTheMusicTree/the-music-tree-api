from bodzify_api.model.criteria.Criteria import Criteria
from .GenreManager import GenreManager


class Genre(Criteria):

    objects: 'GenreManager' = GenreManager()

    class Meta:
        proxy = True
