
from rest_framework import serializers

from bodzify_api.model.user.User import User


class UserDetailedSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['groups', 'user_permissions']
