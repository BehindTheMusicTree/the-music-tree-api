#!/usr/bin/env python

from typing import TypeVar, Generic
from django.db import models

from bodzify_api.model.base.utils.base_model.BaseModel import BaseModel

T = TypeVar('T', bound=BaseModel)


class BaseManager(models.Manager, Generic[T]):
    model: type[T]

    def get_default_ordering(self):
        raise NotImplementedError("get_default_ordering must be implemented in child classes")
