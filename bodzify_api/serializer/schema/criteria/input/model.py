#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.criteria.Criteria import Fields, Criteria


class CriteriaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criteria
        fields = [Fields.USER,
                  Fields.NAME,
                  Fields.PARENT,
                  Fields.TYPE]
