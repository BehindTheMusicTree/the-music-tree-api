from typing import TypeVar, Generic
from django.db import models

T = TypeVar('T', bound='BaseModel')  # type: ignore


class BaseManager(models.Manager, Generic[T]):
    model: type[T]

    def get_default_ordering(self):
        raise NotImplementedError("get_default_ordering must be implemented in child classes")
        
    def create_instance(self, **kwargs) -> T:
        instance = super().create(**kwargs)
        return instance
        
    def update_instance(self, instance: T, **kwargs) -> T:
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance
