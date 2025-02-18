from rest_framework import serializers
from django.utils.translation import gettext as _
from bodzify_api.validator.AppValidationError import AppValidationError
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.model.playlist.children.manual.Fields import Fields as ModelFields


class UniquePerUserNameField(serializers.CharField):
    def __init__(self, model, *args, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)

    def run_validation(self, data):
        value = super().run_validation(data)
        request = self.context.get('request')
        if request and value:
            user = request.user
            if self.model.objects.filter(user=user, name=value).exists():
                raise AppValidationError(
                    field=ModelFields.NAME_PUBLIC,
                    message=_('A playlist with this name already exists'),
                    code=FieldValidationErrorCode.NAME_DUPLICATE
                )
        return value
