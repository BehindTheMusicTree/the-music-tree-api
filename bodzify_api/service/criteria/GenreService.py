#!/usr/bin/env python

from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.service.criteria.CriteriaService import CriteriaService


class GenreService(CriteriaService):
        
    def get_criteria_type_id(self):
        return CRITERIA_TYPES_ID.GENRE
