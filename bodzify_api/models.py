#!/usr/bin/env python

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist, SPECIAL_NAMES as SIMPLE_PLAYLIST_SPECIAL_NAMES
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID


@receiver(post_save, sender=User)
def create_playlists_for_new_user(sender, instance, created, **kwargs):
    if created:
        SimplePlaylist.objects.create(
            playlist=Playlist.objects.create(user=instance),
            name=SIMPLE_PLAYLIST_SPECIAL_NAMES.ALL)
        for criteria_type_id in [CRITERIA_TYPES_ID.GENRE, CRITERIA_TYPES_ID.TAG]:
            CriteriaPlaylist.objects.create(
                playlist=Playlist.objects.create(user=instance),
                criteria=None,
                type_id=criteria_type_id)
