#!/usr/bin/env python

import requests
import random
import string
import os

from django.core.files.base import ContentFile, File

from bodzify_api.model.track.MineTrack import MineTrack
import bodzify_api.myfreemp3_scrapper.scrapper as myfreemp3scrapper
from bodzify_api.service import LibraryTrackService
from bodzify_api import settings

TRACK_TEMP_FILE_INDIVIDUAL_DIRECTORY_NAME_LETTER_TYPE = string.ascii_lowercase
TRACK_TEMP_FILE_INDIVIDUAL_DIRECTORY_NAME_LENGTH = 20


def list(query, pageNumber, pageSize):
    return myfreemp3scrapper.scrap(query, pageNumber, pageSize)


def extract(user, title, artist, duration, releasedOn, mineTrackUrl):
    mineTrack = MineTrack(
        title = title,
        artist = artist,
        duration = duration,
        releasedOn = releasedOn,
        url = mineTrackUrl)

    response = requests.get(mineTrackUrl)

    trackTempFileIndividualDirectoryName = ''.join(
        random.choice(TRACK_TEMP_FILE_INDIVIDUAL_DIRECTORY_NAME_LETTER_TYPE) 
        for i in range(TRACK_TEMP_FILE_INDIVIDUAL_DIRECTORY_NAME_LENGTH))

    trackTempFileIndividualDirectoryAbsolutePath = (
        settings.MEDIA_TEMP + trackTempFileIndividualDirectoryName + "/")

    os.mkdir(trackTempFileIndividualDirectoryAbsolutePath)
    trackDownloadedFilenameWithoutExtension, trackTempfileExtension = (
        os.path.splitext(mineTrackUrl))
    trackTempFileDefinitiveName = artist + " - " + title + trackTempfileExtension
    trackTempFileAbsolutePath = (
        trackTempFileIndividualDirectoryAbsolutePath + trackTempFileDefinitiveName)
    trackFile = open(trackTempFileAbsolutePath, "wb")
    trackFile.write(response.content)

    libraryTrack = LibraryTrackService.CreateFromMineTrack(
        user=user, mineTrack=mineTrack, trackTempFileAbsolutePath=trackTempFileAbsolutePath)
    
    os.remove(trackTempFileAbsolutePath)
    os.rmdir(trackTempFileIndividualDirectoryAbsolutePath)

    return libraryTrack
