#!/usr/bin/env python

from bodzify_api.models import Genre

class GenreDAO:
    def create(user, genreName, parentUuid):
        if parentUuid != None:
            parent = Genre.objects.get(uuid=parentUuid, user=user)
            if parent == None:
                return None
        else:
            parent = None
        if Genre.objects.filter(name=genreName, user=user).exists() == False:
            genre = Genre(name=genreName, parent=parent, user=user)
            genre.save()
            return genre
        else:
            return None

    def getAllByUser(user):
        return Genre.objects.filter(user=user)

    def get(uuid):
        return Genre.objects.get(uuid=uuid)