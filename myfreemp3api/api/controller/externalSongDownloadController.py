import logging
import os
import requests

from mutagen.easyid3 import EasyID3

import myfreemp3api.settings as settings
import myfreemp3api.api.settings as apiSettings
from myfreemp3api.models import SongDB

def downloadExternalSong (user, song):
    userLibraryPath = settings.LIBRARIES_PATH + user.get_username() + "/"

    if not os.path.exists(userLibraryPath):
        os.makedirs(userLibraryPath)

    externalSongUrl = song.url
    externalSong = requests.get(externalSongUrl)
    externalSongName, externalSongExtension = os.path.splitext(externalSongUrl)

    internalSongFilePathWithoutExtension = userLibraryPath + song.artist + " - " + song.title
    internalSongFilePath = internalSongFilePathWithoutExtension + externalSongExtension

    existingFileCount = 0
    while os.path.exists(internalSongFilePath):
        existingFileCount = existingFileCount + 1
        internalSongFilePath = internalSongFilePathWithoutExtension + " (" + str(existingFileCount) + ")" + externalSongExtension


    with open(internalSongFilePath, 'wb') as file:
        file.write(externalSong.content)

    songFile = EasyID3(internalSongFilePath)
    if apiSettings.ID3_TAG_TITLE in songFile:
        title = songFile[apiSettings.ID3_TAG_TITLE]
    else:
        title = ""
    if apiSettings.ID3_TAG_ARTIST in songFile:
        artist = songFile[apiSettings.ID3_TAG_ARTIST]
    else:
        artist = ""
    if apiSettings.ID3_TAG_ALBUM in songFile:
        album = songFile[apiSettings.ID3_TAG_ALBUM]
    else:
        album = ""
    if apiSettings.ID3_TAG_GENRE in songFile:
        genre = songFile[apiSettings.ID3_TAG_GENRE]
    else:
        genre = ""
    if apiSettings.ID3_TAG_DURATION in songFile:
        duration = songFile[apiSettings.ID3_TAG_DURATION]
    else:
        duration = ""
    if apiSettings.ID3_TAG_RATING in songFile:
        rating = songFile[apiSettings.ID3_TAG_RATING]
    else:
        rating = 0
    if apiSettings.ID3_TAG_LANGUAGE in songFile:
        language = songFile[apiSettings.ID3_TAG_LANGUAGE]
    else:
        language = ""

    songDB = SongDB(path = internalSongFilePath, 
        user = user, 
        title = title, 
        artist = artist, 
        album = album, 
        genre = genre, 
        duration = duration,
        rating = rating,
        language = language)
    songDB.save()

    return songDB
