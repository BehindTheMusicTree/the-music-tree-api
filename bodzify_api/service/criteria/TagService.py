#!/usr/bin/env python
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.service.criteria.CriteriaService import CriteriaService


class TagService(CriteriaService):
        
    def get_criteria_type_id(self):
        return CriteriaTypesId.TAG
