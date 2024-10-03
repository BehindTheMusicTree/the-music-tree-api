#!/usr/bin/env python

from bodzify_api.model.criteria.Criteria import Criteria, AttributesLabels
from rest_framework import serializers


class CriteriaModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Criteria
        fields = [AttributesLabels.USER,
                  AttributesLabels.NAME,
                  AttributesLabels.PARENT,
                  AttributesLabels.TYPE]
