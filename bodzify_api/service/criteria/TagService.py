#!/usr/bin/env python

from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.service.criteria.CriteriaService import CriteriaService


class TagService(CriteriaService):

    def __init__(self) -> None:
        super().__init__(CRITERIA_TYPES_ID.TAG)
