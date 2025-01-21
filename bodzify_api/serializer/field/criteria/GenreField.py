from bodzify_api.model.criteria.children.genre.Genre import Genre
from .CriteriaField import CriteriaField


class GenreField(CriteriaField):

    def __init__(self, **kwargs):
        super().__init__(queryset=Genre.objects.all(), **kwargs)
