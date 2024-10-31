
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.service.criteria.GenreService import GenreService
from bodzify_api.view.viewset.model.criteria.CriteriaViewSet import CriteriaViewSet


class GenreViewSet(CriteriaViewSet):
    def __init__(self, **kwargs):
        super().__init__(service=GenreService(), **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(type_id=CriteriaTypesId.GENRE)
