from rest_framework import serializers

from bodzify_api.model.user.User import User

from .Fields import Fields


class UserDetailedSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        Fields = [Fields.ID,
                  Fields.USERNAME,
                  Fields.EMAIL,
                  Fields.IS_TEST_USER,
                  Fields.IS_STAFF,
                  Fields.IS_SUPERUSER,
                  Fields.GROUPS,
                  Fields.USER_PERMISSIONS]
