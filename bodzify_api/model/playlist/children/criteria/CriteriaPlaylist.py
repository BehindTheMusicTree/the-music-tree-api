from typing import TYPE_CHECKING, Dict

from django.db import models

from bodzify_api.model.criteria.Fields import Fields as CriteriaFields
from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypePks
from bodzify_api.model.criteria.type.CriteriaType import CriteriaType
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.field.foreign_key.AppForeignKey import AppForeignKey
from bodzify_api.model.field.foreign_key.PrivateForeignKey import PrivateForeignKey
from bodzify_api.model.field.foreign_key.PrivateOneToOneField import PrivateOneToOneField
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.Fields import Fields as PlaylistFields
from bodzify_api.utils.model import SaveContext
from .CriterialessPlaylistNames import CriterialessPlaylistNames
from .CriteriaPlaylistManager import CriteriaPlaylistManager
from .Fields import Fields


class CriteriaPlaylist(Playlist):
    playlist = PrivateOneToOneField(Playlist,
                                    on_delete=models.CASCADE,
                                    parent_link=True,
                                    related_name=PlaylistFields.CRITERIA_PLAYLIST)
    criteria = PrivateOneToOneField(Criteria,
                                    on_delete=models.CASCADE,
                                    blank=True,
                                    null=True,
                                    related_name=CriteriaFields.CRITERIA_PLAYLIST)
    parent: 'CriteriaPlaylist | None' = PrivateForeignKey(
        'self', on_delete=models.SET_NULL, null=True, related_name=Fields.CHILDREN)  # type: ignore
    root: 'CriteriaPlaylist' = PrivateForeignKey(
        'self', on_delete=models.DO_NOTHING, related_name=Fields.ROOT_DESCENDANTS)  # type: ignore
    type = AppForeignKey(CriteriaType, on_delete=models.CASCADE)

    if TYPE_CHECKING:
        children: models.QuerySet['CriteriaPlaylist']

    objects: CriteriaPlaylistManager = CriteriaPlaylistManager()

    class Meta:
        verbose_name = 'Criteria Playlist'
        verbose_name_plural = 'Criteria Playlists'
        indexes = [models.Index(fields=[Fields.CRITERIA], name='crit_playlist_criteria_idx'),]

    @property
    def type_label(self) -> str:
        return self.type.label

    @property
    def name_when_no_criteria(self) -> str:
        if self.type.pk == CriteriaTypePks.GENRE:
            return CriterialessPlaylistNames.GENRE
        if self.type.pk == CriteriaTypePks.TAG:
            return CriterialessPlaylistNames.TAG
        else:
            raise ValueError(f'Unknown criteria type: {self.type.pk}')

    @property
    def name(self):
        return self.criteria.name if self.criteria else self.name_when_no_criteria

    @property
    def is_root(self) -> bool:
        return self.root == self

    def __str__(self) -> str:
        parent_str = f'Parent: {self.parent.name}' if self.parent else 'Parent: None'
        root_str = f'Root: {self.root.name}' if self.root else 'Root: None'
        return f'{self.uuid} | {self.name} | {parent_str} | {root_str}'

    def _set_parent(self) -> bool:
        current_parent_pk = getattr(self, f"{Fields.PARENT}_id", None)

        if self.criteria and self.criteria.parent:
            parent: CriteriaPlaylist = CriteriaPlaylist.objects.get(criteria=self.criteria.parent)
            if current_parent_pk != parent.pk:
                self.parent = parent
                return True
        elif current_parent_pk is not None:
            self.parent = None
            return True
        return False

    def _set_root(self) -> bool:
        current_root_pk = getattr(self, f"{Fields.ROOT}_pk", None)
        new_root_pk = self.pk if not self.criteria or self.criteria.is_root else self.criteria.root.criteria_playlist.pk

        if current_root_pk != new_root_pk:
            self.root_id = new_root_pk
            return True
        else:
            return False

    def _prepare_save(self, ctx: SaveContext) -> Dict:
        self._set_uuid_if_necessary()
        return ctx.kwargs

    def _perform_save(self, adding: bool, ctx: SaveContext) -> None:
        parent_has_changed = self._set_parent()
        if not adding and parent_has_changed:
            ctx.add_modified_field(Fields.PARENT)

        root_has_changed = self._set_root()
        if not adding and root_has_changed:
            ctx.add_modified_field(f'{Fields.ROOT}_id')

        super()._perform_save(adding=adding, ctx=ctx)

    def _post_save(self, adding: bool) -> None:
        if adding:
            self.root_id = self.pk
            super().save(update_fields=[f'{Fields.ROOT}_id'])
