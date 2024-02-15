#!/usr/bin/env python

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.service.criteria.TagService import TagService
from bodzify_api.view.viewset.criteria.CriteriaViewSet import CriteriaViewSet
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId


class TagViewSet(CriteriaViewSet):

    queryset = Criteria.objects.filter(type_id=CriteriaTypesId.TAG)

    def _get_service(self):
        return TagService()
