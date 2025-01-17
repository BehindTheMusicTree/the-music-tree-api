
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
        transformed_kwargs = transform_name_fields(instance.__class__, **kwargs)

        for key, value in transformed_kwargs.items():
            if hasattr(instance, key):
                field = instance._meta.get_field(key)
                if isinstance(field, models.ManyToManyField):
                    getattr(instance, key).set(value)
                else:
                    setattr(instance, key, value)
            else:
                raise ValueError(f"Field {key} does not exist in {instance.__class__.__name__}")

        instance.save()
        instance.refresh_from_db()  # Otherwise, foreign objects' fields may not be updated
        return instance

    def delete_instance(self, instance: T):
        raise NotImplementedError()
