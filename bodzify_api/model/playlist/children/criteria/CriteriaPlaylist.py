from abc import abstractmethod
from typing import Dict, Any, TYPE_CHECKING

from django.db import models

from bodzify_api import settings
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.Fields import Fields as CriteriaFields
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from bodzify_api.utils.model import SaveContext
from bodzify_api.model.criteria.type.CriteriaType import CriteriaType
from .CriteriaPlaylistManager import CriteriaPlaylistManager
from .Fields import Fields


class CriteriaPlaylist(BasePlaylist):
    criteria = models.OneToOneField(Criteria,
                                    on_delete=models.CASCADE,
                                    blank=True,
                                    null=True,
                                    related_name=CriteriaFields.CRITERIA_PLAYLIST_DB)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name=Fields.CHILDREN)
    root = models.ForeignKey('self', on_delete=models.DO_NOTHING, related_name=Fields.DESCENDANTS)
    type = models.ForeignKey(CriteriaType, on_delete=models.CASCADE)

    objects: CriteriaPlaylistManager = CriteriaPlaylistManager()

    class Meta:
        db_table = f'{settings.APP_NAME}_criteria_playlist'
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
    def children(self) -> models.QuerySet['CriteriaPlaylist']:
        return CriteriaPlaylist.objects.get_children(self.user, self)

    def __str__(self) -> str:
        return f'{self.name}'

    def _prepare_save(self, **kwargs) -> Dict[str, Any]:
        ctx = SaveContext(
            kwargs=kwargs,
            modified_fields=[],
            update_fields=kwargs.get('update_fields')
        )

        parent_has_changed = self._set_parent()
        if parent_has_changed and not self._state.adding:
            ctx.add_modified_field(Fields.PARENT)

        root_has_changed = self._set_root()
        if root_has_changed and not self._state.adding:
            ctx.add_modified_field(Fields.ROOT)

        if ctx.modified_fields and not ctx.should_track_fields:
            ctx.kwargs['update_fields'] = ctx.modified_fields

        return ctx.kwargs

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
        current_root_pk = getattr(self, f"{Fields.ROOT}_id", None)

        if self.criteria and self.criteria.root:
            try:
                root = CriteriaPlaylist.objects.get(criteria=self.criteria.root)
                if current_root_pk != root.pk:
                    self.root = root
                    return True
            except CriteriaPlaylist.DoesNotExist:
                pass
        return False

    def _post_save(self):
        if not self._state.adding:
            self._post_update()

    def _post_update(self):
        current_root_id = getattr(self, f"{Fields.ROOT}_id", None)
        if self._original_root != current_root_id:
            self._update_children_root()

    def _update_children_root(self):
        for child in self.children:
            child.root = self.root
            child.save(update_fields=[Fields.ROOT])

    def save(self, *args, **kwargs):
        if self._state.adding:
            super().save(*args, **kwargs)
            self.root = self
            super().save(update_fields=['root'])

        kwargs = self._prepare_save(**kwargs)
        super().save(*args, **kwargs)
        self._post_save()
