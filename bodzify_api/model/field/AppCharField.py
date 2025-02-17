from django.db import models


class AppCharField(models.CharField):
    """
    Custom CharField model field that uses AppCharField serializer for serialization.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from bodzify_api.serializer.field.AppCharField import AppCharField
        self.serializer_field_class = AppCharField

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # Ensure Django uses the correct path for migrations
        path = 'bodzify_api.model.field.AppCharField'
        return name, path, args, kwargs
