#!/usr/bin/env python

from django.db import models
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CriteriaType, CRITERIA_TYPES_ID
from bodzify_api.model.playlist.Playlist import Playlist, ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL


class SPECIAL_NAMES:
    GENRELESS = 'Genreless'
    TAGLESS = 'Tagless'


class TYPES_LABEL:
    GENRE = 'genre'
    TAG = 'tag'


class ATTRIBUTES_LABEL:
    PLAYLIST = 'playlist'
    PARENT = 'parent'
    CRITERIA = 'criteria'
    NAME = 'name'
    ROOT = 'root'


class CriteriaPlaylist(models.Model):
    playlist = models.OneToOneField(Playlist,
                                    on_delete=models.CASCADE,
                                    primary_key=True,
                                    related_name=PLAYLIST_ATTRIBUTES_LABEL.CRITERIA_PLAYLIST)
    criteria = models.OneToOneField(Criteria,
                                    on_delete=models.CASCADE,
                                    blank=True,
                                    null=True,
                                    related_name=PLAYLIST_ATTRIBUTES_LABEL.CRITERIA_PLAYLIST)
    type = models.ForeignKey(CriteriaType, on_delete=models.CASCADE, blank=True, null=False)

    # null must be True because when the root is the criteria playlist itself, we must create it first with a null root
    # and then set the root to itself
    parent = models.ForeignKey('CriteriaPlaylist', on_delete=models.CASCADE, null=True, related_name='child_playlist')
    root = models.ForeignKey('CriteriaPlaylist', on_delete=models.CASCADE,
                             null=True, related_name='descendant_playlist')

    @property
    def name(self):
        if self.criteria is None:
            if self.type.pk == CRITERIA_TYPES_ID.GENRE:
                return SPECIAL_NAMES.GENRELESS
            elif self.type.pk == CRITERIA_TYPES_ID.TAG:
                return SPECIAL_NAMES.TAGLESS
        else:
            return self.criteria.name

    def __str__(self) -> str:
        return f'{str(self.playlist.uuid)} {self.name}'

    def _set_parent(self):
        if self.criteria is None:
            self.parent = None
        elif self.criteria.parent is None:
            self.parent = None
        else:
            self.parent = self.criteria.parent.criteria_playlist  # type: ignore

    def _set_root(self):
        if self.criteria:
            self.root = self.criteria.root.criteria_playlist
        else:
            self.root = self

    def _create(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._set_root()
        super().save(update_fields=[ATTRIBUTES_LABEL.ROOT])

    def _update(self, old_criteria_playlist: 'CriteriaPlaylist', *args, **kwargs):
        super().save(*args, **kwargs)

        if self.criteria:
            print('isrootdifferent ' + str(self.root.criteria != self.criteria.root))
            if self.root.criteria != self.criteria.root:  # type: ignore
                self._set_root()
                super().save(update_fields=[ATTRIBUTES_LABEL.ROOT])
                self._update_root_of_children(criteria_playlist=self, new_root=self.root)  # type: ignore

    def _update_root_of_children(self, criteria_playlist: 'CriteriaPlaylist', new_root: 'CriteriaPlaylist'):
        criteria_playlist.root = new_root  # type: ignore
        children = criteria_playlist.get_children()
        if children.exists():
            for child in children:
                child.root = new_root
                child.save()

    def get_children(self):
        return CriteriaPlaylist.objects.filter(parent=self)

    def save(self, *args, **kwargs):
        print('save playlist ' + str(self))
        self._set_parent()
        try:
            old_criteria_playlist = CriteriaPlaylist.objects.get(playlist__uuid=self.playlist.uuid)
            self._update(old_criteria_playlist, *args, **kwargs)  # type: ignore
        except CriteriaPlaylist.DoesNotExist:
            self._create(*args, **kwargs)
