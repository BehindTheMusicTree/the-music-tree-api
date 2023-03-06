#!/usr/bin/env python
from django.db import models


class RatingSourcesLabelInRatingTag:
    NoSource = ''
    Bodzify = 'bodzify'
    MusicBee = 'MusicBee'
    WindowsMediaPlayer = 'Windows Media Player 9 Series'
    Traktor = 'traktor@native-instruments.d'
    Itunes = 'iTunes'

class RatingSourcesIds:
    NoSource = 0
    Bodzify = 1
    Other = 2
    MusicBee = 3
    WindowsMediaPlayer = 4
    Winamp = 5
    Itunes = 6


class RatingSource(models.Model):
    label = models.CharField(unique=True, max_length=20, default=None, editable=False)
    labelInRatingTag = models.CharField(unique=True, max_length=20, default=None, editable=False)
    noStarRating = models.IntegerField(default=None, editable=False)
    zeroStarRating = models.IntegerField(default=None, editable=False)
    oneStarRating = models.IntegerField(default=None, editable=False)
    twoStarsRating = models.IntegerField(default=None, editable=False)
    threeStarsRating = models.IntegerField(default=None, editable=False)
    fourStarsRating = models.IntegerField(default=None, editable=False)

    def __str__(self) -> str:
        return str(self.id) + " " + self.label