from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.service.criteria.GenreService import GenreService
from bodzify_api.view.viewset.model.criteria.CriteriaViewSet import CriteriaViewSet
from django.db.models import Q


class GenreViewSet(CriteriaViewSet):
    def __init__(self, **kwargs):
        super().__init__(criteria_type_id=CriteriaTypesId.GENRE, **kwargs)
