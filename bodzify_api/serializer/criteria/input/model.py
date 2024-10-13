#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.criteria.Criteria import AttributesLabels, Criteria


class CriteriaModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Criteria
        fields = [AttributesLabels.USER,
                  AttributesLabels.NAME,
                  AttributesLabels.PARENT,
                  AttributesLabels.TYPE]
