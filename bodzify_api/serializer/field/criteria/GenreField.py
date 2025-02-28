from typing import Optional, List

from bodzify_api.model.criteria.children.genre.Genre import Genre
from bodzify_api.serializer.field.criteria.CriteriaField import CriteriaField


class GenreField(CriteriaField):
    def __init__(self, input_types: Optional[List[str]] = None, **kwargs):
        super().__init__(queryset=Genre.objects.all(), input_types=input_types, **kwargs)
