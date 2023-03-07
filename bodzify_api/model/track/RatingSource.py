#!/usr/bin/env python
from django.db import models


class RatingSourcesLabelInRatingTag:
    NONE = ''
    BODZIFY = 'bodzify'
    MUSICBEE = 'MusicBee'
    WMP = 'Windows Media Player 9 Series'
    TRAKTOR = 'traktor@native-instruments.d'
    ITUNES = 'iTunes'


class RatingSourcesIds:
    NONE = 0
    BODZIFY = 1
    OTHER = 2
    MUSICBEE = 3
    WMP = 4
    TRAKTOR = 5
    WINAMP = 6
    ITUNES = 7


class RatingSource(models.Model):
    label = models.CharField(unique=True, max_length=20, default=None, editable=False)
    labelInRatingTag = models.CharField(unique=True, max_length=20, default=None, editable=False)
    noRating = models.IntegerField(default=None, editable=False, null=True)
    zeroStarRating = models.IntegerField(default=None, editable=False)
    oneStarRating = models.IntegerField(default=None, editable=False)
    twoStarsRating = models.IntegerField(default=None, editable=False)
    threeStarsRating = models.IntegerField(default=None, editable=False)
    fourStarsRating = models.IntegerField(default=None, editable=False)

    def __str__(self) -> str:
        return str(self.id) + " " + self.label