from typing import Self, TypeVar

from django.db import models

from bodzify_api.model.base.BaseManager import BaseManager
from bodzify_api.model.base.DynamicTableNameModelBase import DynamicTableNameModelBase
from bodzify_api.model.lib_track_mixin.query_utils import transform_name_fields
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
        return SaveContext.create(**kwargs)

    def save(self, *args, **kwargs):
        adding = self._state.adding
        ctx = self._create_save_context(**kwargs)
        kwargs = self._prepare_save(ctx)
        self._perform_save(adding=adding, ctx=ctx)
        if ctx.modified_fields and not ctx.should_track_fields:
            kwargs['update_fields'] = ctx.modified_fields
        super().save(*args, **kwargs)
        self._post_save(adding=adding)

    def _prepare_save(self, ctx: SaveContext) -> dict:
        # Transform name fields if needed
        transformed_kwargs = transform_name_fields(self.__class__, **ctx.kwargs)
        ctx.kwargs = transformed_kwargs
        return ctx.kwargs

    def _perform_save(self, adding: bool, ctx: SaveContext) -> None:
        pass

    def _post_save(self, adding: bool) -> None:
        pass
