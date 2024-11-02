from typing import Self, TypeVar, Generic
from django.db import models

from bodzify_api.model.base.utils.base_model.BaseManager import BaseManager

T = TypeVar('T', bound='BaseModel')

class BaseModel(models.Model):
    objects: BaseManager[Self]

    class Meta:
        abstract = True

    @staticmethod
    def ensure_update_field(kwargs: dict, field_name: str) -> dict:
        if 'update_fields' not in kwargs:
            kwargs['update_fields'] = [field_name]
        elif kwargs['update_fields'] is not None:
            if field_name not in kwargs['update_fields']:
                kwargs['update_fields'].append(field_name)
        return kwargs

    @staticmethod
    def ensure_update_fields(kwargs: dict, field_names: list[str]) -> dict:
        if 'update_fields' not in kwargs:
            kwargs['update_fields'] = field_names
        elif kwargs['update_fields'] is not None:
            for field in field_names:
                if field not in kwargs['update_fields']:
                    kwargs['update_fields'].append(field)
        return kwargs
