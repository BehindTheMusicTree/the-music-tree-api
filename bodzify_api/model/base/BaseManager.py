
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

    def get_or_create(self, *args, **kwargs) -> Any:
        transformed_kwargs = transform_name_fields(self.model, **kwargs)
        return super().get_or_create(*args, **transformed_kwargs)

    def create(self, **kwargs) -> T:
        transformed_kwargs = transform_name_fields(self.model, **kwargs)
        return super().create(**transformed_kwargs)

    def filter(self, *args: Any, **kwargs: Any) -> QuerySet[T]:
        transformed_kwargs = transform_name_fields(self.model, **kwargs)
        return super().filter(*args, **transformed_kwargs)

    def update_instance(self, instance: T, **kwargs) -> T:
        # Initialize dictionaries for different types of updates
        save_kwargs = {}
        many_to_many_updates = {}
        regular_updates = {}

        # Separate fields based on their type and purpose
        for key, value in kwargs.items():
            if key in ['update_fields', 'force_insert', 'force_update', 'using']:
                save_kwargs[key] = value
            else:
                if hasattr(instance, key):
                    field = instance._meta.get_field(key)
                    if isinstance(field, models.ManyToManyField):
                        many_to_many_updates[key] = value
                    else:
                        regular_updates[key] = value
                else:
                    raise ValueError(f"Field {key} does not exist in {instance.__class__.__name__}")

        # Update regular fields
        for key, value in regular_updates.items():
            setattr(instance, key, value)

        # Save the instance with regular updates
        save_kwargs['update_fields'] = list(regular_updates.keys())
        instance.save(**save_kwargs)

        # Handle M2M fields after save
        for key, value in many_to_many_updates.items():
            getattr(instance, key).set(value)
        instance.refresh_from_db()  # Refresh the instance to get the updated M2M fields
        return instance

    def delete_instance(self, instance: T):
        raise NotImplementedError()
