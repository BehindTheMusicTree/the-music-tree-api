from typing import Optional, List

from api.model.criteria.children.genre.Genre import Genre
from api.serializer.field.criteria.CriteriaField import CriteriaField


class GenreField(CriteriaField):
    """
    Genre-specific field that inherits from the unified CriteriaField.
    Automatically handles both UUID and name-based inputs for genres.
    """

    def __init__(self, input_types: Optional[List[str]] = None, **kwargs):
        super().__init__(
            queryset=Genre.objects.all(),
            input_types=input_types,
            **kwargs
        )

    def to_representation(self, value):
        return super().to_representation(value)
