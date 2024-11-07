from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.children.genre.GenreManager import GenreManager


class Genre(Criteria):

    objects: 'GenreManager' = GenreManager()

    class Meta:
        proxy = True
