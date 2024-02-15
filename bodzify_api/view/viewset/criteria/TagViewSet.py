#!/usr/bin/env python

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.service.criteria.TagService import TagService
from bodzify_api.view.viewset.criteria.CriteriaViewSet import CriteriaViewSet
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID


class TagViewSet(CriteriaViewSet):

    queryset = Criteria.objects.filter(type_id=CRITERIA_TYPES_ID.TAG)

    def __init__(self, **kwargs):
        super().__init__(TagService(), **kwargs)
