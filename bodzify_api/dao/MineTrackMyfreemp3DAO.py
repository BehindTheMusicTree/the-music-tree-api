#!/usr/bin/env python

import os
import requests

import bodzify_api.settings as settings
from bodzify_api.models import LibraryTrack

import bodzify_api.myfreemp3_scrapper.scrapper as myfreemp3scrapper

class MineTrackMyfreemp3DAO:
    def list(query, pageNumber, pageSize):
        return myfreemp3scrapper.scrap(query, pageNumber, pageSize)

    def extract(user, title, artist, duration, releaseOn, mineTrackUrl):
        userLibraryPath = settings.LIBRARIES_PATH + user.get_username() + "/"

        if not os.path.exists(userLibraryPath):
            os.makedirs(userLibraryPath)

        externalTrackFile = requests.get(mineTrackUrl)
        externalTrackName, trackExtension = os.path.splitext(mineTrackUrl)

        artistTitle = artist + " - " + title
        libraryFilename = artistTitle + trackExtension
        internalTrackFilePath = userLibraryPath + libraryFilename

        existingFileCount = 0
        while os.path.exists(internalTrackFilePath):
            existingFileCount = existingFileCount + 1
            libraryFilename = artistTitle + " (" + str(existingFileCount) + ")" + trackExtension
            internalTrackFilePath = userLibraryPath + libraryFilename

        with open(internalTrackFilePath, 'wb') as file:
            file.write(externalTrackFile.content)

        # Tags of every myfreemp3 downloaded tracks are empty 
        libraryTrack = LibraryTrack(
            path=internalTrackFilePath,
            user=user, 
            title=title, 
            artist=artist, 
            album="", 
            genre=None, 
            duration=duration,
            rating=-1,
            language="")
        libraryTrack.save()

        return libraryTrack
