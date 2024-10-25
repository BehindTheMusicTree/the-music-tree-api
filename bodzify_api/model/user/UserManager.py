#!/usr/bin/env python

from typing import Generic, TypeVar, TYPE_CHECKING

from django.contrib.auth.models import BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

from bodzify_api.model.AllLibTrackMixin import AllLibTrackMixin
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId

if TYPE_CHECKING:
    from bodzify_api.model.user.User import User, Fields as ModelFields
    from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist

T = TypeVar('T', bound='User')  # type: ignore


class UserManager(BaseUserManager, Generic[T]):
    def create_user(self, username, email, password=None, **extra_fields):

        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user: User = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)
