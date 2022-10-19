#!/usr/bin/env python

import os
import requests

import myfreemp3api.settings as settings
from myfreemp3api.models import SongDB

import myfreemp3api.myfreemp3scrapper.scrapper as myfreemp3scrapper

class ExternalSongMyfreemp3DAO:
    def get_list(query, pageNumber):
        return myfreemp3scrapper.scrap(query, pageNumber)

    def download(user, title, artist, duration, date, externalSongUrl):
        userLibraryPath = settings.LIBRARIES_PATH + user.get_username() + "/"

        if not os.path.exists(userLibraryPath):
            os.makedirs(userLibraryPath)

        externalSongFile = requests.get(externalSongUrl)
        externalSongName, externalSongExtension = os.path.splitext(externalSongUrl)

        internalSongFilePathWithoutExtension = userLibraryPath + artist + " - " + title
        internalSongFilePath = internalSongFilePathWithoutExtension + externalSongExtension

        existingFileCount = 0
        while os.path.exists(internalSongFilePath):
            existingFileCount = existingFileCount + 1
            internalSongFilePath = internalSongFilePathWithoutExtension + " (" + str(existingFileCount) + ")" + externalSongExtension


        with open(internalSongFilePath, 'wb') as file:
            file.write(externalSongFile.content)

        # Tags of every myfreemp3 downloaded songs are empty 
        songDB = SongDB(path = internalSongFilePath, 
            user = user, 
            title = title, 
            artist = artist, 
            album = "", 
            genre = "", 
            duration = duration,
            rating = None,
            language = "")
        songDB.save()

        return songDB
