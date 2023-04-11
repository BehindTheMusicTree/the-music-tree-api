#!/usr/bin/env python
from rest_framework import serializers
from bodzify_api.model.criteria.Criteria import Criteria, ATTRIBUTES_LABEL
from bodzify_api.serializer.criteria.CriteriaSimpleSerializer import CriteriaSimpleSerializer
from bodzify_api.serializer.criteria.CriteriaTypeSerializer import CriteriaTypeSerializer


class CriteriaDetailedSerializer(serializers.ModelSerializer):

    type = CriteriaTypeSerializer()
    parent = CriteriaSimpleSerializer()

    class Meta:
        model = Criteria
        fields = [ATTRIBUTES_LABEL.UUID, 
                  ATTRIBUTES_LABEL.NAME, 
                  ATTRIBUTES_LABEL.PARENT, 
                  ATTRIBUTES_LABEL.TYPE, 
                  ATTRIBUTES_LABEL.ADDED_ON]
