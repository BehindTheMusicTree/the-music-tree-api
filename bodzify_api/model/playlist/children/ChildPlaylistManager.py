#!/usr/bin/env python

from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from bodzify_api.model.playlist.children.ChildPlaylist import Fields
    from bodzify_api.model.playlist.BasePlaylist import BasePlaylist


class ChildPlaylistManager(models.Manager):

    def filter(self, *args, **kwargs):
        if Fields.UUID in kwargs:
            kwargs[f'{Fields.BASE_PLAYLIST}__{Fields.UUID}'] = kwargs.pop(Fields.UUID)
        if Fields.USER in kwargs:
            kwargs[f'{Fields.BASE_PLAYLIST}__{Fields.USER}'] = kwargs.pop(Fields.USER)
        return super().filter(*args, **kwargs)

    def get(self, *args, **kwargs):
        if Fields.UUID in kwargs:
            kwargs[f'{Fields.BASE_PLAYLIST}__{Fields.UUID}'] = kwargs.pop(Fields.UUID)
        if Fields.USER in kwargs:
            kwargs[f'{Fields.BASE_PLAYLIST}__{Fields.USER}'] = kwargs.pop(Fields.USER)
        return super().get(*args, **kwargs)

    def create(self, *args, **kwargs):

        model_class = self.model
        if model_class._meta.abstract:
            raise ValueError(f"Cannot create an instance of abstract class {model_class.__name__}")

        user = kwargs.pop(Fields.USER, None)
        if user is None:
            raise ValueError("User must be provided when creating a ChildPlaylist")

        base_playlist = BasePlaylist.objects.create(user=user)
        print(f'Created base playlist {base_playlist.uuid} for user {user.username}')
        kwargs[Fields.BASE_PLAYLIST] = base_playlist

        return super().create(*args, **kwargs)

    def get_or_create(self, **kwargs):
        if Fields.UUID in kwargs:
            kwargs[f'{Fields.BASE_PLAYLIST}__{Fields.UUID}'] = kwargs.pop(Fields.UUID)
        if Fields.USER in kwargs:
            kwargs[f'{Fields.BASE_PLAYLIST}__{Fields.USER}'] = kwargs.pop(Fields.USER)
        return super().get_or_create(**kwargs)
