from abc import abstractmethod
from typing import Dict, Any

from django.db import models

from bodzify_api import settings
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.utils.model import SaveContext
from ..ChildPlaylist import ChildPlaylist
from .CriteriaPlaylistManager import CriteriaPlaylistManager
from .Fields import Fields


class CriteriaPlaylist(ChildPlaylist):
    criteria = models.OneToOneField(Criteria, on_delete=models.CASCADE, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name=Fields.CHILD_PLAYLIST)
    root = models.ForeignKey('self', on_delete=models.SET_NULL, related_name=Fields.DESCENDANT_PLAYLIST)

    objects: CriteriaPlaylistManager = CriteriaPlaylistManager()

    class Meta:
        db_table = f'{settings.APP_NAME}_criteria_playlist'
        indexes = [models.Index(fields=[Fields.BASE_PLAYLIST, Fields.CRITERIA], name='%(class)s_idx'),]

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

    def _prepare_save(self, is_creating, **kwargs) -> Dict[str, Any]:
        ctx = SaveContext(
            kwargs=kwargs,
            modified_fields=[],
            update_fields=kwargs.get('update_fields')
        )

        parent_has_changed = self._set_parent()
        if parent_has_changed and not is_creating:
            ctx.add_modified_field(Fields.PARENT)

        root_has_changed = self._set_root()
        if root_has_changed and not is_creating:
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

    def _is_creating(self) -> bool:
        return getattr(self, f"{Fields.ROOT}_id", None) is None

    def _post_save(self, is_creating: bool):
        if not is_creating:
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
        is_creating = self._is_creating()
        if is_creating:
            self.root = self

        kwargs = self._prepare_save(is_creating, **kwargs)
        super().save(*args, **kwargs)
        self._post_save(is_creating=is_creating)
