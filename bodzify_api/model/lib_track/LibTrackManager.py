from django.db import models

from bodzify_api.model.base.BaseQuerySet import BaseQuerySet
from bodzify_api.model.lib_track.Fields import Fields


class LibraryTrackQuerySet(BaseQuerySet):
    def for_user(self, user):
        return self.filter(**{Fields.USER: user})

    def by_name(self, name):
        return self.filter(**{Fields.NAME: name})

    def by_artist(self, artist):
        return self.filter(**{Fields.ARTIST: artist})

    def by_album(self, album):
        return self.filter(**{Fields.ALBUM: album})

    def by_genre(self, genre):
        return self.filter(**{Fields.GENRE: genre})

    def by_tag(self, tag):
        return self.filter(**{Fields.TAG: tag})


class LibTrackManager(models.Manager):
    def get_queryset(self):
        return LibraryTrackQuerySet(self.model, using=self._db)

    def for_user(self, user):
        return self.get_queryset().for_user(user)

    def by_name(self, name):
        return self.get_queryset().by_name(name)

    def by_artist(self, artist):
        return self.get_queryset().by_artist(artist)

    def by_album(self, album):
        return self.get_queryset().by_album(album)

    def by_genre(self, genre):
        return self.get_queryset().by_genre(genre)

    def by_tag(self, tag):
        return self.get_queryset().by_tag(tag)
