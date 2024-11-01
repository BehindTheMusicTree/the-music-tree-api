
from typing import TYPE_CHECKING, Optional

from attr import has
from django.db import models
from django.db.models import QuerySet, Manager

from bodzify_api import settings
from bodzify_api.model.LibTrackMixin import LibTrackMixin, Fields as LibTrackMixinFields
from bodzify_api.model.criteria.CriteriaManager import CriteriaManager
from bodzify_api.model.criteria.CriteriaType import CriteriaType

if TYPE_CHECKING:
    from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist


class Fields:
    MODEL = 'Criteria'
    CREATED_ON = LibTrackMixinFields.CREATED_ON
    UPDATED_ON = LibTrackMixinFields.UPDATED_ON
    USER = LibTrackMixinFields.USER
    UUID = LibTrackMixinFields.UUID
    LIB_TRACKS = LibTrackMixinFields.LIB_TRACKS
    LIB_TRACKS_NOT_ARCHIVED = LibTrackMixinFields.LIB_TRACKS_NOT_ARCHIVED
    LIB_TRACKS_COUNT = LibTrackMixinFields.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = LibTrackMixinFields.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = LibTrackMixinFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = LibTrackMixinFields.DURATION_STR_IN_HOUR_MIN_SEC
    NAME = 'name'
    TYPE = 'type'
    PARENT = 'parent'
    CHILD = 'child'
    ASCENDANT = 'ascendant'
    ASCENDANTS = ASCENDANT + 's'
    DESCENDANT = 'descendant'
    DESCENDANTS = DESCENDANT + 's'
    CRITERIA_ASCENDANT_RELATION_ASCENDANTS = 'criteria_ascendant_relation_ascendants'
    CRITERIA_ASCENDANT_RELATION_DESCENDANTS = 'criteria_ascendant_relation_descendants'
    CHILDREN = 'children'
    ROOT = 'root'
    CRITERIA_PLAYLIST = 'criteria_playlist'


class Criteria(LibTrackMixin):
    name = models.CharField(max_length=settings.CRITERIA_NAME_LEN_MAX, default=None)
    type = models.ForeignKey(CriteriaType, on_delete=models.CASCADE)
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               null=True,
                               related_name=Fields.CHILD)
    ascendants = models.ManyToManyField(Fields.MODEL,
                                        through='CriteriaAscendantRel',
                                        related_name=Fields.MODEL + 's')
    root = models.ForeignKey('self',
                             on_delete=models.CASCADE,
                             related_name=Fields.DESCENDANT)

    objects: CriteriaManager = CriteriaManager()

    class Meta:
        constraints = [models.CheckConstraint(check=~models.Q(name=""), name='criteria_non_empty_name')]
        indexes = [
            models.Index(fields=[Fields.USER, Fields.NAME], name='criteria_user_name_idx'),
            models.Index(fields=[Fields.USER, Fields.UUID], name='criteria_user_uuid_idx')
        ]

    @property
    def criteria_playlist(self) -> 'CriteriaPlaylist':
        return self.criteria_playlist

    @property
    def children(self) -> QuerySet['Criteria']:
        return Criteria.objects.filter(user=self.user, parent=self)

    @property
    def criteria_ascendant_relation_ascendants(self) -> Manager:
        return self.criteria_ascendant_relation_ascendants

    def __str__(self) -> str:
        parent_str = f'{Fields.PARENT}: {self.parent.name}' if self.parent else f"[no {Fields.PARENT}]"
        return f"{self.uuid} | {self.name} | {parent_str}"

    @ staticmethod
    def get_common_criteria(criteria_a: Optional['Criteria'], criteria_b: Optional['Criteria']) -> Optional['Criteria']:
        if not criteria_a or not criteria_b:
            return None

        visited = set()
        current = criteria_a
        while current:
            visited.add(current)
            current = current.parent

        current = criteria_b
        while current:
            if current in visited:
                return current
            current = current.parent

        return None

    def calculate_root(self):
        self.root = self.parent.root if self.parent else self

    def is_descendant_of(self, other_criteria: 'Criteria') -> bool:
        if self.parent == other_criteria:
            return True
        elif self.parent:
            return self.parent.is_descendant_of(other_criteria)
        return False

    def _is_creating(self) -> bool:
        return getattr(self, f"{Fields.ROOT}_id", None) is None

    def save(self, *args, **kwargs):
        if self._is_creating():
            if self.parent:
                self.root = self.parent.root
            else:
                self.root = self
        super().save(*args, **kwargs)
