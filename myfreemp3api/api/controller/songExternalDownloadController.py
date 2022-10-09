import os
from os import path
import requests
import logging

import myfreemp3api.settings as settings

def downloadExternalSong (user, externalSongUrl):
    userLibraryPath = settings.LIBRARIES_PATH + user.get_username() + "/"

    if not path.exists(userLibraryPath):
        os.makedirs(userLibraryPath)

    externalSong = requests.get(externalSongUrl)

    externalSongNameParts = externalSongUrl.split("/")
    externalSongName = externalSongNameParts[len(externalSongNameParts) - 1]

    logger = logging.getLogger("info")
    logger.info("username : " + user.get_username())
    logger.info("user : " + str(user))

    with open(userLibraryPath + externalSongName, 'wb') as file:
        file.write(externalSong.content)
