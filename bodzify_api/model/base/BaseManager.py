from typing import TypeVar, Generic, TYPE_CHECKING

from django.db import models


if TYPE_CHECKING:
    from .BaseModel import BaseModel


T = TypeVar('T', bound='BaseModel')  # type: ignore


class BaseManager(models.Manager, Generic[T]):
    model: type[T]

    def get_default_ordering(self):
        raise NotImplementedError()

    def create(self, **kwargs) -> T:
        return super().create(**kwargs)

    def update(self, instance: T, **kwargs) -> T:
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance
