#!/usr/bin/env python
from rest_framework import serializers
from bodzify_api.model.criteria.Criteria import Criteria, ATTRIBUTES_LABEL


class CriteriaSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Criteria
        fields = [ATTRIBUTES_LABEL.UUID, 
                  ATTRIBUTES_LABEL.NAME,
                  ATTRIBUTES_LABEL.ADDED_ON]
