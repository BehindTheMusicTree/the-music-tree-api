#!/usr/bin/env python

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.service.criteria.TagService import TagService
from bodzify_api.view.viewset.model.criteria.CriteriaViewSet import CriteriaViewSet


class TagViewSet(CriteriaViewSet):
    def __init__(self, **kwargs):
        super().__init__(
            service=TagService(),
            model_class=Criteria,
            **kwargs
        )

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(type_id=CriteriaTypesId.TAG)
