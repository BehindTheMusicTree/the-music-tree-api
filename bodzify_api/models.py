#!/usr/bin/env python

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist, SpecialNames as SIMPLE_PLAYLIST_SPECIAL_NAMES
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId


@receiver(post_save, sender=User)
def create_playlists_for_new_user(sender, instance, created, **kwargs):
    if created:
        SimplePlaylist.objects.create(base_playlist=BasePlaylist.objects.create(user=instance),
                                      name=SIMPLE_PLAYLIST_SPECIAL_NAMES.ALL)
        for criteria_type_id in [CriteriaTypesId.GENRE, CriteriaTypesId.TAG]:
            criteria_playlist = CriteriaPlaylist.objects.create(
                base_playlist=BasePlaylist.objects.create(user=instance),
                criteria=None, type_id=criteria_type_id)
            criteria_playlist.root = criteria_playlist  # type: ignore
            criteria_playlist.save()
