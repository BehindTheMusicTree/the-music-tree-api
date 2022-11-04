#!/usr/bin/env python

from bodzify_api.models import Genre

class GenreDAO:
    def create(user, genreName, parentUuid):
        parentGenre = Genre.objects.get(uuid=parentUuid, user=user)
        if parentGenre != None:
            if Genre.objects.filter(name=genreName, user=user).exists() == False:
                genre = Genre(name=genreName, parent=parentGenre, user=user)
                genre.save()
                return genre
            else:
                return None
        else:
            return None

    def getAllByUser(user):
        return Genre.objects.filter(user=user)