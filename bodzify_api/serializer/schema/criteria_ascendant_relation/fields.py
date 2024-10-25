#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.criteria.CriteriaAscendantRel import Fields as ModelFields

class Fields:
    DESCENDANT = ModelFields.DESCENDANT
    ASCENDANT = ModelFields.ASCENDANT
    DEGREE = ModelFields.DEGREE
