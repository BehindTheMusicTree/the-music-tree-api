#!/usr/bin/env python

import os
import requests

import bodzify_api.settings as settings
from bodzify_api.models import LibrarySong

import bodzify_api.myfreemp3_scrapper.scrapper as myfreemp3scrapper


def get_list(query, pageNumber):

    return myfreemp3scrapper.scrap(query, pageNumber)

def download(user, title, artist, duration, releaseDate, mineSongUrl):

    userLibraryPath = settings.LIBRARIES_PATH + user.get_username() + "/"

    if not os.path.exists(userLibraryPath):
        os.makedirs(userLibraryPath)

    externalSongFile = requests.get(mineSongUrl)
    externalSongName, songExtension = os.path.splitext(mineSongUrl)

    artistTitle = artist + " - " + title
    libraryFilename = artistTitle + songExtension
    internalSongFilePath = userLibraryPath + libraryFilename

    existingFileCount = 0
    while os.path.exists(internalSongFilePath):
        existingFileCount = existingFileCount + 1
        libraryFilename = artistTitle + " (" + str(existingFileCount) + ")" + songExtension
        internalSongFilePath = userLibraryPath + libraryFilename

    with open(internalSongFilePath, 'wb') as file:
        file.write(externalSongFile.content)

    # Tags of every myfreemp3 downloaded songs are empty 
    librarySong = LibrarySong(
        path=internalSongFilePath,
        url=
        user=user, 
        title=title, 
        artist=artist, 
        album="", 
        genre="", 
        duration=duration,
        rating=None,
        language="")
    librarySong.save()

    return librarySong
