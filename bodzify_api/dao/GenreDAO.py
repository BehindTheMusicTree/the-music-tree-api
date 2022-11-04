#!/usr/bin/env python

import logging

from bodzify_api.models import Genre

class GenreDAO:
    def create(genre):
        if Genre.objects.filter(name=genre.name, user=genre.user).exists() == False:
            genre.save()
            return genre
        else:
            return None

    def getAllByUser(user):
        return Genre.objects.filter(user=user)