#!/usr/bin/env python

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.service.criteria.GenreService import GenreService
from bodzify_api.view.viewset.model.criteria.CriteriaViewSet import \
    CriteriaViewSet


class GenreViewSet(CriteriaViewSet):

    queryset = Criteria.objects.filter(type_id=CriteriaTypesId.GENRE)

    def __init__(self, **kwargs):
        super().__init__(GenreService(), **kwargs)
