import logging
import os
import requests

from mutagen.easyid3 import EasyID3

import myfreemp3api.settings as settings
import myfreemp3api.api.settings as apiSettings
from myfreemp3api.models import SongDB

def downloadExternalSong (user, externalSong):
    userLibraryPath = settings.LIBRARIES_PATH + user.get_username() + "/"

    if not os.path.exists(userLibraryPath):
        os.makedirs(userLibraryPath)

    externalSongUrl = externalSong.url
    externalSongFile = requests.get(externalSongUrl)
    externalSongName, externalSongExtension = os.path.splitext(externalSongUrl)

    internalSongFilePathWithoutExtension = userLibraryPath + externalSong.artist + " - " + externalSong.title
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
        title = "", 
        artist = "", 
        album = "", 
        genre = "", 
        duration = externalSong.duration,
        rating = None,
        language = "")
    songDB.save()

    return songDB
