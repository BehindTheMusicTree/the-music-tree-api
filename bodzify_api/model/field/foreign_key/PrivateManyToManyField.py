from bodzify_api.model.field.foreign_key.AppManyToManyField import AppManyToManyField
from bodzify_api.serializer.field.foreign_key.PrivateUuidField import PrivateUuidField


class PrivateManyToManyField(AppManyToManyField):
    def __init__(self, to, **kwargs):
        super().__init__(to, **kwargs)
        self.serializer_field_class = PrivateUuidField
