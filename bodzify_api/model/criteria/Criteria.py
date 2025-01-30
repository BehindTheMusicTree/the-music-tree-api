
from typing import TYPE_CHECKING, Any, Optional

from django.db import models, IntegrityError
from django.db.models import QuerySet
from django.utils.translation import gettext as _

from bodzify_api import settings
from bodzify_api.utils.validation_error_utils import raise_validation_error
from bodzify_api.view.error.ValidationResponseCode import ValidationResponseCode
from bodzify_api.model.criteria.CriteriaManager import CriteriaManager
from bodzify_api.model.lib_track_mixin.LibTrackMixin import LibTrackMixin
from bodzify_api.model.criteria.lineage_rel.Fields import Fields as CriteriaLineageRelFields
from bodzify_api.utils.model import SaveContext
from .type.CriteriaType import CriteriaType
from .Fields import Fields

if TYPE_CHECKING:
    from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
    from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
    from .lineage_rel.CriteriaLineageRel import CriteriaLineageRel


class Criteria(LibTrackMixin):
    _name = models.CharField(max_length=settings.CRITERIA_NAME_LEN_MAX, db_column=Fields.NAME_PUBLIC)
    ascendants: QuerySet['Criteria'] = models.ManyToManyField('self',
                                                              through='CriteriaLineageRel',
                                                              through_fields=(CriteriaLineageRelFields.DESCENDANT,
                                                                              CriteriaLineageRelFields.ASCENDANT),
                                                              symmetrical=False,)  # type: ignore
    parent: Optional['Criteria'] = models.ForeignKey('self',
                                                     on_delete=models.SET_NULL,
                                                     null=True,
                                                     related_name=Fields.CHILDREN)  # type: ignore
    root: 'Criteria' = models.ForeignKey('self',
                                         on_delete=models.DO_NOTHING,
                                         related_name=Fields.DESCENDANTS)  # type: ignore
    type = models.ForeignKey(CriteriaType, on_delete=models.CASCADE)

    if TYPE_CHECKING:
        ascendants_rels: QuerySet['CriteriaLineageRel']
        descendants: QuerySet['Criteria']
        descendants_rels: QuerySet['CriteriaLineageRel']
        children: QuerySet['Criteria']
        criteria_playlist: 'CriteriaPlaylist'

    objects: CriteriaManager = CriteriaManager()

    @property
    def name(self) -> str:
        return self._name

    @property
    def lib_tracks(self) -> models.QuerySet['LibraryTrack']:
        return getattr(self, Fields.LIB_TRACKS_RELATED_NAME)

    @property
    def is_root(self) -> bool:
        return not self.parent

    class Meta:
        verbose_name = 'Criteria'
        verbose_name_plural = 'Criterias'
        constraints = [
            models.CheckConstraint(check=~models.Q(_name=""), name='%(class)s_non_empty_name'),
            models.UniqueConstraint(fields=[Fields.USER, Fields.NAME_INTERNAL], name='unique_name_per_user')
        ]
        indexes = [
            models.Index(fields=[Fields.USER, Fields.NAME_INTERNAL], name='%(class)s_user_name_idx'),
            models.Index(fields=[Fields.USER, Fields.UUID], name='%(class)s_user_uuid_idx')
        ]

    def __str__(self) -> str:
        parent_str = f'{Fields.PARENT}: {self.parent.name}' if self.parent else f"[no {Fields.PARENT}]"
        created_on_str = f"{Fields.CREATED_ON}: {self.created_on}"
        updated_on_str = f"{Fields.UPDATED_ON}: {self.updated_on}"

        return f"{self.uuid} | {self.name} | {parent_str} | {created_on_str} | {updated_on_str}"

    def _set_root(self):
        current_root = getattr(self, f"{Fields.ROOT}", None)
        new_root = self.parent.root if self.parent else self

        new_root_pk = None
        if not new_root:
            new_root_pk = self.pk
        elif current_root != new_root:
            new_root_pk = new_root.pk

        if new_root_pk:
            self.root_id = new_root_pk
            return True
        return False

    def _prepare_save(self, ctx: SaveContext) -> dict:
        self._set_uuid_if_necessary()
        root_has_changed = self._set_root()
        if not self._state.adding and root_has_changed:
            ctx.add_modified_field(f'{Fields.ROOT}_id')
        return ctx.kwargs

    def save(self, *args: Any, **kwargs: Any) -> None:
        try:
            super().save(*args, **kwargs)
        except IntegrityError as e:
            error_message = str(e)
            if 'non_empty_name' in error_message:
                raise_validation_error(
                    message=_('Name cannot be empty'),
                    code=ValidationResponseCode.FIELD_NAME_EMPTY.value,
                    field='name'
                )
            elif 'unique_name_per_user' in error_message:
                raise_validation_error(
                    message=_('A criteria with this name already exists for this user'),
                    code=ValidationResponseCode.FIELD_NAME_DUPLICATE.value,
                    field='name'
                )
            else:
                raise_validation_error(
                    message=_('Database integrity error occurred'),
                    code=ValidationResponseCode.FIELD_DB_INTEGRITY_ERROR.value,
                    field='non_field_errors'
                )

    def is_descendant_of(self, other_criteria: 'Criteria') -> bool:
        if self.parent == other_criteria:
            return True
        elif self.parent:
            return self.parent.is_descendant_of(other_criteria)
        return False
