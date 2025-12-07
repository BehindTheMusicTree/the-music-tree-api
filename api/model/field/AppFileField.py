from django.db import models


class AppFileField(models.FileField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from api.serializer.field.AppFileField import AppFileField
        self.serializer_field_class = AppFileField

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        path = 'api.model.field.AppFileField'
        return name, path, args, kwargs
