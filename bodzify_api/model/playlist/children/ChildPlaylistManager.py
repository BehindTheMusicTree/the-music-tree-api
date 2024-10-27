#!/usr/bin/env python

from typing import TYPE_CHECKING

from django.db import models
from django.core.exceptions import ValidationError
from bodzify_api.model.playlist.children.Fields import Fields as ModelFields


class ChildPlaylistManager(models.Manager):

    def filter(self, *args, **kwargs):
        if ModelFields.UUID in kwargs:
            kwargs[f'{ModelFields.BASE_PLAYLIST}__{ModelFields.UUID}'] = kwargs.pop(ModelFields.UUID)
        if ModelFields.USER in kwargs:
            kwargs[f'{ModelFields.BASE_PLAYLIST}__{ModelFields.USER}'] = kwargs.pop(ModelFields.USER)
        return super().filter(*args, **kwargs)

    def get(self, *args, **kwargs):
        if ModelFields.UUID in kwargs:
            kwargs[f'{ModelFields.BASE_PLAYLIST}__{ModelFields.UUID}'] = kwargs.pop(ModelFields.UUID)
        if ModelFields.USER in kwargs:
            kwargs[f'{ModelFields.BASE_PLAYLIST}__{ModelFields.USER}'] = kwargs.pop(ModelFields.USER)
        return super().get(*args, **kwargs)

    def get_or_create(self, **kwargs):
        if ModelFields.UUID in kwargs:
            kwargs[f'{ModelFields.BASE_PLAYLIST}__{ModelFields.UUID}'] = kwargs.pop(ModelFields.UUID)
        if ModelFields.USER in kwargs:
            kwargs[f'{ModelFields.BASE_PLAYLIST}__{ModelFields.USER}'] = kwargs.pop(ModelFields.USER)
        return super().get_or_create(**kwargs)

    def create(self, user, *args, **kwargs):
        from bodzify_api.model.playlist.BasePlaylist import BasePlaylist

        model_class = self.model
        if model_class._meta.abstract:
            raise ValueError(f"Cannot create an instance of abstract class {model_class.__name__}")

        if not user:
            raise ValueError("User must be provided when creating a ChildPlaylist")

        base_playlist = kwargs.pop(ModelFields.BASE_PLAYLIST, None)
        if base_playlist:
            raise ValidationError("base_playlist must not be provided when creating a ChildPlaylist")

        base_playlist = BasePlaylist.objects.create(user=user)
        kwargs[ModelFields.BASE_PLAYLIST] = base_playlist

        return super().create(*args, **kwargs)
