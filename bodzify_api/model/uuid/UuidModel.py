import uuid

from django.db import models

from bodzify_api.model.base.BaseModel import BaseModel


class UuidModel(BaseModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True

    def _set_uuid_if_necessary(self):
        if self._state.adding and not self.pk:
            self.pk = uuid.uuid4()
            while self.__class__.objects.filter(pk=self.pk).exists():
                self.pk = uuid.uuid4()
