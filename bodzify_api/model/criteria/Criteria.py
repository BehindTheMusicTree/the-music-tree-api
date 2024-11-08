from typing import TYPE_CHECKING, Any, Dict, Optional

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
    from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
    from .lineage_rel.CriteriaLineageRel import CriteriaLineageRel


class Criteria(LibTrackMixin):
    name = models.CharField(max_length=settings.CRITERIA_NAME_LEN_MAX, default=None)
    _ascendants = models.ManyToManyField('self',
                                         through='CriteriaLineageRel',
                                         through_fields=(CriteriaLineageRelFields.DESCENDANT,
                                                         CriteriaLineageRelFields.ASCENDANT),
                                         symmetrical=False,)
    _parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name=Fields.CHILDREN)
    _root = models.ForeignKey('self', on_delete=models.DO_NOTHING, related_name=Fields.DESCENDANTS)
    type = models.ForeignKey(CriteriaType, on_delete=models.CASCADE)

    objects: CriteriaManager = CriteriaManager()

    @property
    def library_tracks(self) -> models.QuerySet['LibraryTrack']:
        return getattr(self, Fields.LIB_TRACKS_DB)

    # Only for type hinting
    @property
    def ascendants(self) -> QuerySet['Criteria']:
        return self._ascendants

    @ property
    def parent(self) -> Optional['Criteria']:
        return self._parent

    @ property
    def root(self) -> 'Criteria':
        return self._root

    @ property
    def criteria_playlist(self) -> 'CriteriaPlaylist':
        return getattr(self, Fields.CRITERIA_PLAYLIST_DB)

    @ property
    def children(self) -> QuerySet['Criteria']:
        return self.__class__.objects.filter(user=self.user, parent=self)

    @ property
    def ascendants_rel(self) -> QuerySet['CriteriaLineageRel']:
        return self._ascendants_rel.all()  # type: ignore

    @ property
    def descendants_rel(self) -> QuerySet['CriteriaLineageRel']:
        return self._descendants_rel.all()  # type: ignore

    @property
    def is_root(self) -> bool:
        return self.root == self

    class Meta:
        verbose_name = 'Criteria'
        verbose_name_plural = 'Criterias'
        constraints = [models.CheckConstraint(check=~models.Q(name=""), name='%(class)s_non_empty_name')]
        indexes = [
            models.Index(fields=[Fields.USER, Fields.NAME], name='%(class)s_user_name_idx'),
            models.Index(fields=[Fields.USER, Fields.UUID], name='%(class)s_user_uuid_idx')
        ]

    def __str__(self) -> str:
        parent_str = f'{Fields.PARENT}: {self.parent.name}' if self.parent else f"[no {Fields.PARENT}]"
        return f"{self.uuid} | {self.name} | {parent_str}"

    def _set_root(self):
        current_root_pk = getattr(self, f"{Fields.ROOT_DB}_pk", None)
        new_root_pk = self.parent.root.pk if self.parent else None

        if current_root_pk != new_root_pk:
            self.root_id = new_root_pk
            return True
        else:
            return False

    def _prepare_save(self, **kwargs) -> Dict[str, Any]:
        self._set_pk_if_necessary()
        ctx = __class__._create_save_context(**kwargs)

        root_has_changed = self._set_root()
        if not self._state.adding and root_has_changed:
            ctx.add_modified_field(f'{Fields.ROOT_DB}_pk')

        if ctx.modified_fields and not ctx.should_track_fields:
            ctx.kwargs['update_fields'] = ctx.modified_fields

        return ctx.kwargs

    def is_descendant_of(self, other_criteria: 'Criteria') -> bool:
        if self.parent == other_criteria:
            return True
        elif self.parent:
            return self.parent.is_descendant_of(other_criteria)
        return False

    def save(self, *args, **kwargs):
        kwargs = self._prepare_save(**kwargs)
        super().save(*args, **kwargs)
