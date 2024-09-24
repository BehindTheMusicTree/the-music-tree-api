#!/usr/bin/env python

from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.service.criteria.CriteriaService import CriteriaService


class TagService(CriteriaService):

    def __init__(self) -> None:
        super().__init__(CriteriaTypesId.TAG)
