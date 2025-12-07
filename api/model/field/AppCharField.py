from django.db import models


class AppCharField(models.CharField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from api.serializer.field.AppCharField import AppCharField
        self.serializer_field_class = AppCharField

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # Ensure Django uses the correct path for migrations
        path = 'api.model.field.AppCharField'
        return name, path, args, kwargs
