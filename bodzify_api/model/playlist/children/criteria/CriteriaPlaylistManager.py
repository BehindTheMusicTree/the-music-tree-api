#!/usr/bin/env python

from typing import TYPE_CHECKING
from django.db import models, transaction
from django.db.models import QuerySet
from typing import Optional

from bodzify_api.model.playlist.children.ChildPlaylistManager import ChildPlaylistManager

if TYPE_CHECKING:
    from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
    from bodzify_api.model.criteria.Criteria import Criteria
    from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist, Fields as ModelFields
    from bodzify_api.model.LibTrackMixin import SpecialNames


class CriteriaPlaylistManager(ChildPlaylistManager):
    def get_children(self, user, parent) -> QuerySet['CriteriaPlaylist']:
        return self.filter(user=user, parent=parent)

    def get_by_name(self, user, name: str) -> Optional['CriteriaPlaylist']:
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
