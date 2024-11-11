from dataclasses import Field
from queue import Empty
from typing import Any, Dict, Generic, TypeVar, TYPE_CHECKING

from django.contrib.auth.models import BaseUserManager
from django.http import QueryDict
from .Fields import Fields

if TYPE_CHECKING:
    from bodzify_api.model.user.User import User


class UserManager(BaseUserManager):
    model: 'User'

    def create_instance(self, **kwargs) -> 'User':
        from bodzify_api.model.user.User import User
        # data = kwargs
        # if kwargs is Empty:
        #     data: Dict[str, Any] = {}
        # elif isinstance(kwargs, dict):
        #     data: Dict[str, Any] = kwargs
        # elif isinstance(kwargs, QueryDict):
        #     data: Dict[str, Any] = kwargs.dict()
        # else:
        #     data: Dict[str, Any] = {}
        if not kwargs[Fields.EMAIL]:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(kwargs.pop(Fields.EMAIL))
        password = kwargs.pop(Fields.PASSWORD)

        user: User = User(username=kwargs.pop(Fields.USERNAME), email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields) -> 'User':
        extra_fields.setdefault(Fields.IS_STAFF, True)
        extra_fields.setdefault(Fields.IS_SUPERUSER, True)

        if extra_fields.get(Fields.IS_STAFF) is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get(Fields.IS_SUPERUSER) is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_instance(username=username, email=email, password=password, **extra_fields)
