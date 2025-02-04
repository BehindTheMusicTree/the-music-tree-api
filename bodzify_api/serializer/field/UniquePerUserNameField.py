from rest_framework import serializers
from django.utils.translation import gettext as _
from bodzify_api.utils.validation_error_utils import raise_validation_error
from bodzify_api.view.error.FieldValidationErrorCode import FieldValidationErrorCode
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
                raise_validation_error(
                    message=_('A playlist with this name already exists'),
                    field_validation_error_code=FieldValidationErrorCode.FIELD_PLAYLIST_NAME_DUPLICATE,
                    field=ModelFields.NAME_PUBLIC
                )
        return value