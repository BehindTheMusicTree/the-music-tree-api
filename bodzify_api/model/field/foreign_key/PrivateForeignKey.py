from bodzify_api.model.field.foreign_key.AppForeignKey import AppForeignKey
from bodzify_api.serializer.field.foreign_key.PrivateUuidField import \
    PrivateUuidField


class PrivateForeignKey(AppForeignKey):
    def __init__(self, to, **kwargs):
        super().__init__(to, **kwargs)
        self.serializer_field_class = PrivateUuidField
