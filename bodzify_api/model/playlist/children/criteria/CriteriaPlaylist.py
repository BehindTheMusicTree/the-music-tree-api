from abc import abstractmethod
from typing import Dict, Any, TYPE_CHECKING, Optional

from django.db import models

from bodzify_api.model.criteria.Fields import Fields as CriteriaFields
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from bodzify_api.model.criteria.type.CriteriaType import CriteriaType
from bodzify_api.model.criteria.Criteria import Criteria
from .CriteriaPlaylistManager import CriteriaPlaylistManager
from .Fields import Fields


class CriteriaPlaylist(BasePlaylist):
    criteria = models.OneToOneField(Criteria,
                                    on_delete=models.CASCADE,
                                    blank=True,
                                    null=True,
                                    related_name=CriteriaFields.CRITERIA_PLAYLIST)
    parent: Optional['CriteriaPlaylist'] = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, related_name=Fields.CHILDREN)  # type: ignore
    root: 'CriteriaPlaylist' = models.ForeignKey(
        'self', on_delete=models.DO_NOTHING, related_name=Fields.ROOT_DESCENDANTS)  # type: ignore
    type = models.ForeignKey(CriteriaType, on_delete=models.CASCADE)

    if TYPE_CHECKING:
        children: models.QuerySet['CriteriaPlaylist']

    objects: CriteriaPlaylistManager = CriteriaPlaylistManager()

    class Meta:
        verbose_name = 'Criteria Playlist'
        verbose_name_plural = 'Criteria Playlists'
        indexes = [models.Index(fields=[Fields.CRITERIA], name='crit_playlist_criteria_idx'),]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_parent = getattr(self, f"{Fields.PARENT}_id", None)
        self._original_root = getattr(self, f"{Fields.ROOT}_id", None)

    @abstractmethod
    def name_when_no_criteria() -> str:
        raise NotImplementedError()

    @property
    def name(self):
        return self.criteria.name if self.criteria else self.name_when_no_criteria()

    @property
    def is_root(self) -> bool:
        return self.root == self

    def __str__(self) -> str:
        return f'{self.uuid} | {self.name} | {self.parent} | {self.root}'

    def _set_parent(self) -> bool:
        current_parent_pk = getattr(self, f"{Fields.PARENT}_id", None)

        if self.criteria and self.criteria.parent:
            parent = CriteriaPlaylist.objects.get(criteria=self.criteria.parent)
            if current_parent_pk != parent.pk:
                self.parent = parent
                return True
        elif current_parent_pk is not None:
            self.parent = None
            return True
        return False

    def _set_root(self) -> bool:
        current_root_pk = getattr(self, f"{Fields.ROOT}_pk", None)

        if not self.criteria or self.criteria.is_root:
            new_root_pk = self.pk
        else:
            new_root_pk = self.criteria.root.criteria_playlist.pk

        if current_root_pk != new_root_pk:
            self.root_id = new_root_pk
            return True
        else:
            return False

    def _prepare_save(self, **kwargs) -> Dict[str, Any]:
        self._set_uuid_if_necessary()
        ctx = __class__._create_save_context(**kwargs)

        parent_has_changed = self._set_parent()
        if not self._state.adding and parent_has_changed:
            ctx.add_modified_field(Fields.PARENT)

        root_has_changed = self._set_root()
        if not self._state.adding and root_has_changed:
            ctx.add_modified_field(f'{Fields.ROOT}_pk')

        if ctx.modified_fields and not ctx.should_track_fields:
            ctx.kwargs['update_fields'] = ctx.modified_fields

        return ctx.kwargs

    def _post_save(self, adding: bool):
        if adding:
            self.root_id = self.pk
            super().save(update_fields=[f'{Fields.ROOT}_id'])

    def save(self, *args, **kwargs):
        adding = self._state.adding
        kwargs = self._prepare_save(**kwargs)
        super().save(*args, **kwargs)
        self._post_save(adding=adding)
