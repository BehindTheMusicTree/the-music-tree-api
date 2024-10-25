#!/usr/bin/env python

from typing import TYPE_CHECKING

from django.db import models, transaction
from django.db.models import QuerySet
from django.core.exceptions import ValidationError
from typing import Optional, cast

from bodzify_api.model.criteria.CriteriaType import CriteriaType

if TYPE_CHECKING:
    from bodzify_api.model.criteria.Criteria import Criteria
    from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist, Fields as ModelFields
    from bodzify_api.model.LibTrackMixin import SpecialNames


class CriteriaPlaylistManager(models.Manager):
    def get_children(self, user, parent) -> models.QuerySet['CriteriaPlaylist']:  # type: ignore
        return self.filter(user=user, parent=parent)

    def _set_parent(self, instance: 'CriteriaPlaylist'):
        if instance.criteria is None:
            instance.parent = None
        elif instance.criteria.parent is None:
            instance.parent = None
        else:
            instance.parent = instance.criteria.parent.criteria_playlist

    def _set_root(self, instance: 'CriteriaPlaylist'):
        if instance.criteria:
            if instance.criteria.root is None:
                raise ValidationError("Criteria must have a root")
            if not hasattr(instance.criteria.root, 'criteria_playlist'):
                raise ValidationError("Root criteria must have an associated playlist")
            instance.root = cast(models.Model, instance.criteria.root.criteria_playlist)
        else:
            instance.root = instance

    def _update_root_of_children(self, instance: 'CriteriaPlaylist', new_root):
        instance.root = new_root
        children: QuerySet[CriteriaPlaylist] = self.get_children(instance.user, instance)
        if children.exists():
            for child in children:
                child.root = new_root
                child.save()

    def _create(self, instance: 'CriteriaPlaylist', *args, **kwargs):
        instance.save(*args, **kwargs)
        self._set_root(instance)
        instance.save(update_fields=[ModelFields.ROOT])

    def _update(self, instance: 'CriteriaPlaylist', *args, **kwargs):
        instance.save(*args, **kwargs)

        if instance.criteria:
            current_root_criteria = getattr(instance.root, ModelFields.ROOT, None)
            if current_root_criteria != instance.criteria.root:
                self._set_root(instance)
                instance.save(update_fields=[ModelFields.ROOT])
                self._update_root_of_children(instance, instance.root)

    @transaction.atomic
    def create(self, user, type, criteria: Optional['Criteria'] = None, base_playlist=None):

        if base_playlist and self.filter(base_playlist=base_playlist).exists():
            raise ValueError("Playlist with this base_playlist already exists")

        playlist: CriteriaPlaylist = self.model(
            user=user,
            type=CriteriaType.objects.get(pk=type),
            criteria=criteria,
            base_playlist=base_playlist
        )

        self._set_parent(playlist)
        self._create(playlist)

        if criteria is None:
            playlist.root = playlist
            playlist.save(update_fields=[ModelFields.ROOT])

        return playlist

    @transaction.atomic
    def update(self, base_playlist, **kwargs):
        playlist = self.get(base_playlist=base_playlist)

        for field, value in kwargs.items():
            setattr(playlist, field, value)

        self._set_parent(playlist)
        self._update(playlist)

        return playlist

    def get_by_name(self, user, name: str) -> Optional['CriteriaPlaylist']:  # type: ignore
        return self.filter(user=user).filter(
            models.Q(criteria__name=name) |
            models.Q(
                criteria__isnull=True,
                type__in=[
                    models.Q(name=SpecialNames.GENRELESS) |
                    models.Q(name=SpecialNames.TAGLESS)
                ]
            )
        ).first()
