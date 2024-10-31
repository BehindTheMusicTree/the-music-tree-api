
from typing import TypeVar, Generic
from django.db import models

T = TypeVar('T', bound='bodzify_api.model.base.utils.base_model.BaseModel.BaseModel')


class BaseManager(models.Manager, Generic[T]):
    model: type[T]

    def get_default_ordering(self):
        raise NotImplementedError("get_default_ordering must be implemented in child classes")
