from typing import Self, TypeVar

from django.db import models

from bodzify_api.model.base.BaseManager import BaseManager
from bodzify_api.model.base.DynamicTableNameModelBase import DynamicTableNameModelBase
from bodzify_api.utils.model import SaveContext

T = TypeVar('T', bound='BaseModel')


class BaseModel(models.Model, metaclass=DynamicTableNameModelBase):
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

    @staticmethod
    def _create_save_context(**kwargs):
        return SaveContext(kwargs=kwargs, modified_fields=[], update_fields=kwargs.get('update_fields'))
