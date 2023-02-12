#!/usr/bin/env python
import shortuuid
from django.db import models
from django.contrib.auth.models import User
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class Album(models.Model):
    # Django's UUIDField won't validate a shortuuid
    uuid = models.CharField(
            primary_key=True, default=shortuuid.uuid, max_length=22, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default=None)
    year = models.CharField(max_length=4, default=None, null=True)
    albumArtists = models.ManyToManyField('bodzify_api.Artist')

    def delete(self):
        artists = list(self.albumArtists.all())
        super(Album, self).delete()
        if artists is not None:
            for artist in artists:
                if Album.objects.filter(user=self.user, albumArtists__in=[artist]).count() == 0:
                    if LibraryTrack.objects.filter(user=self.user, artist=artist).count() == 0:
                        artist.delete()
