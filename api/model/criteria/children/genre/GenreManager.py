from typing import TYPE_CHECKING


from ...CriteriaManager import CriteriaManager


if TYPE_CHECKING:
    from .Genre import Genre


class GenreManager(CriteriaManager):
    model: 'Genre'
