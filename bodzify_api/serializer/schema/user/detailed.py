#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.user.User import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['groups', 'user_permissions']
