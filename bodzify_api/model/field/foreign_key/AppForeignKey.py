from django.db import models


class AppForeignKey(models.ForeignKey):
    """
    Custom ForeignKey model field that uses ForeignKeyField serializer for serialization.
    """

    def __init__(self, to, **kwargs):
        super().__init__(to, **kwargs)
        from bodzify_api.serializer.field.foreign_key.ForeignKeyField import \
            ForeignKeyField
        self.serializer_field_class = ForeignKeyField
