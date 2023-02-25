#!/usr/bin/env python
import requests
import random
import string
import os
from django.http.request import QueryDict
from django.contrib.auth.models import User
from bodzify_api.model.track.MineTrack import MineTrack
import bodzify_api.myfreemp3_scrapper.scrapper as myfreemp3scrapper
from bodzify_api.service import TrackService
from bodzify_api import settings

TRACK_TEMP_FILE_INDIVIDUAL_DIR_NAME_LENGTH = 20


def List(query, pageNumber, pageSize):
    return myfreemp3scrapper.scrap(query, pageNumber, pageSize)


def _getTrackTempFileIndividualDirAbsPath():
    trackTempFileIndividualDirName = (
            _generateShortUU(TRACK_TEMP_FILE_INDIVIDUAL_DIR_NAME_LENGTH))

    trackTempFileIndividualDirAbsPath = settings.MEDIA_TEMP + trackTempFileIndividualDirName + "/"

    os.makedirs(trackTempFileIndividualDirAbsPath)

    return trackTempFileIndividualDirAbsPath

def _getTrackTempFileAbsPath(trackTempFileIndividualDirAbsPath, mineTrackUrl):
    trackDownloadedFilenameWithoutExtension, trackTempfileExtension = (
            os.path.splitext(mineTrackUrl))
    return (trackTempFileIndividualDirAbsPath 
            + trackDownloadedFilenameWithoutExtension + trackTempfileExtension)
    

def _generateShortUU(length: int):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def _getLastPartOfUrl(url):
    return url.split("/")[-1]


def _writeResponseToTempFile(trackTempFileAbsPath, response):
    trackFile = open(trackTempFileAbsPath, "wb")
    trackFile.write(response.content)
    return trackTempFileAbsPath


def Extract(user: User, requestData: QueryDict):
    mineTrackUrl = requestData[MineTrack.ATTRIBUTE_URL_LABEL]

    trackTempFileIndividualDirAbsPath = _getTrackTempFileIndividualDirAbsPath()
    trackTempFileAbsPath = trackTempFileIndividualDirAbsPath + _getLastPartOfUrl(mineTrackUrl)
    _writeResponseToTempFile(trackTempFileAbsPath, requests.get(mineTrackUrl))

    libraryTrack = TrackService.CreateFromMineExtract(
        user=user, requestData=requestData, trackTempFileAbsPath=trackTempFileAbsPath)
    
    os.remove(trackTempFileAbsPath)
    os.rmdir(trackTempFileIndividualDirAbsPath)

    return libraryTrack
