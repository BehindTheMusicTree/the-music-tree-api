
from typing import TypeVar, Generic, TYPE_CHECKING, Any

from django.db import models
from django.db.models import QuerySet

from bodzify_api.model.utils.query import transform_name_fields


if TYPE_CHECKING:
    from .BaseModel import BaseModel


T = TypeVar('T', bound='BaseModel')  # type: ignore


class BaseManager(models.Manager, Generic[T]):
    model: type[T]

    def get_default_ordering(self):
        raise NotImplementedError()

    def get(self, *args: Any, **kwargs: Any) -> Any:
        transformed_kwargs = transform_name_fields(self.model, **kwargs)
        return super().get(*args, **transformed_kwargs)

    def create(self, **kwargs) -> T:
        transformed_kwargs = transform_name_fields(self.model, **kwargs)
        return super().create(**transformed_kwargs)

    def filter(self, *args: Any, **kwargs: Any) -> QuerySet[T]:
        transformed_kwargs = transform_name_fields(self.model, **kwargs)
        return super().filter(*args, **transformed_kwargs)

    def update_instance(self, instance: T, **kwargs) -> T:
        print('instance before update', instance)

        # Separate model field updates from save kwargs
        save_kwargs = {}
        field_updates = {}

        print('kwargs', kwargs)
        for key, value in kwargs.items():
            if key in ['update_fields', 'force_insert', 'force_update', 'using']:
                save_kwargs[key] = value
            else:
                field_updates[key] = value
        print('field updates', field_updates)

        # Update instance fields
        for key, value in field_updates.items():
            if hasattr(instance, key):
                field = instance._meta.get_field(key)
                if isinstance(field, models.ManyToManyField):
                    getattr(instance, key).set(value)
                else:
                    setattr(instance, key, value)
            else:
                raise ValueError(f"Field {key} does not exist in {instance.__class__.__name__}")

        print('instance after update', instance)
        save_kwargs['update_fields'] = list(field_updates.keys())
        instance.save(**save_kwargs)
        print('save kwargs', save_kwargs)
        print('instance after save', instance)
        instance.refresh_from_db()
        print('instance after refresh', instance)
        return instance

    def delete_instance(self, instance: T):
        raise NotImplementedError()
