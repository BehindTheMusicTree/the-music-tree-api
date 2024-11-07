from typing import TYPE_CHECKING, Optional, Self

from django.db import models
from django.db.models import QuerySet

from bodzify_api import settings
from bodzify_api.model.criteria.CriteriaManager import CriteriaManager
from bodzify_api.model.lib_track_mixin.LibTrackMixin import LibTrackMixin
from bodzify_api.model.criteria.lineage_rel.Fields import Fields as CriteriaLineageRelFields
from .type.CriteriaType import CriteriaType
from .Fields import Fields

if TYPE_CHECKING:
    from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
    from .lineage_rel.CriteriaLineageRel import CriteriaLineageRel


class Criteria(LibTrackMixin):
    name = models.CharField(max_length=settings.CRITERIA_NAME_LEN_MAX, default=None)
    ascendants = models.ManyToManyField('self',
                                        through='CriteriaLineageRel',
                                        through_fields=(CriteriaLineageRelFields.DESCENDANT,
                                                        CriteriaLineageRelFields.ASCENDANT),
                                        symmetrical=False,)

    root_degree = models.PositiveIntegerField(default=0)
    type = models.ForeignKey(CriteriaType, on_delete=models.CASCADE)

    objects: CriteriaManager = CriteriaManager()

    class Meta:
        db_table = f'{settings.APP_NAME}_criteria'
        verbose_name = 'Criteria'
        verbose_name_plural = 'Criterias'
        constraints = [models.CheckConstraint(check=~models.Q(name=""), name='%(class)s_non_empty_name')]
        indexes = [
            models.Index(fields=[Fields.USER, Fields.NAME], name='%(class)s_user_name_idx'),
            models.Index(fields=[Fields.USER, Fields.UUID], name='%(class)s_user_uuid_idx')
        ]

    @ property
    def root(self) -> 'Criteria':
        if self.root_degree == 0:
            return self
        root_ascendant_rel = self.ascendants_rel.filter(degree=self.root_degree).first()
        if not root_ascendant_rel:
            raise ValueError(f'Root not well set for {self}')
        return root_ascendant_rel.ascendant

    @ property
    def parent(self) -> Optional['Criteria']:
        from .lineage_rel.CriteriaLineageRel import CriteriaLineageRel
        try:
            ascendant_rel = self.ascendants_rel.get(degree=1)
            return ascendant_rel.ascendant
        except CriteriaLineageRel.DoesNotExist:
            return None

    @ property
    def criteria_playlist(self) -> 'CriteriaPlaylist':
        return self._criteria_playlist  # type: ignore

    @ property
    def children(self) -> QuerySet['Criteria']:
        return self.__class__.objects.filter(user=self.user, parent=self)

    @ property
    def ascendants_rel(self) -> QuerySet['CriteriaLineageRel']:
        return self._ascendants_rel.all()  # type: ignore

    @ property
    def descendants_rel(self) -> QuerySet['CriteriaLineageRel']:
        return self._descendants_rel.all()  # type: ignore

    def __str__(self) -> str:
        parent_str = f'{Fields.PARENT}: {self.parent.name}' if self.parent else f"[no {Fields.PARENT}]"
        return f"{self.uuid} | {self.name} | {parent_str}"

    @ staticmethod
    def get_common_criteria(criteria_a: Optional['Criteria'],
                            criteria_b: Optional['Criteria']) -> Optional['Criteria']:
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

    def calculate_root_degree(self):
        parent = self.parent
        self.root_degree = parent.root_degree + 1 if parent else 0

    def is_descendant_of(self, other_criteria: 'Criteria') -> bool:
        if self.parent == other_criteria:
            return True
        elif self.parent:
            return self.parent.is_descendant_of(other_criteria)
        return False

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.calculate_root_degree()
        super().save(*args, **kwargs)
