#!/usr/bin/env python
import pprint
import requests
import random
import string
import os
from django.core.files.temp import NamedTemporaryFile
from django.core import files
from django.core.files.base import File
from django.http.request import QueryDict
from django.contrib.auth.models import User
from bodzify_api import settings
import bodzify_api.service.TrackService as TrackService
from bodzify_api.model.track.MineTrack import MineTrack
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.criteria.Criteria import CriteriaSpecialNames
import bodzify_api.myfreemp3_scrapper.scrapper as myfreemp3scrapper
from bodzify_api.serializer.track.input.TrackUpdateSchemaSerializer import TrackUpdateSchemaSerializer


TRACK_TEMP_FILE_INDIVIDUAL_DIR_NAME_LENGTH = 20


def List(query, pageNumber, pageSize):
    return myfreemp3scrapper.Scrap(query, pageNumber, pageSize)


def Extract(user: User, requestData: QueryDict):
    mineTrackUrl = requestData[MineTrack.ATTRIBUTE_URL_LABEL]
    trackInMemoryFile = requests.get(mineTrackUrl, stream=True)
    with NamedTemporaryFile(delete=True) as trackTempFile:
        for block in trackInMemoryFile.iter_content(1024 * 8):
            if not block:
                break
            trackTempFile.write(block)
        trackTempFile.flush()
        trackTempFile.seek(0)

        saveData = _getSaveDataFromRequestData(requestData)

        trackFileName = _getTrackFileName(mineTrackUrl, requestData)
        saveData[LibraryTrack.ATTRIBUTE_FILE_LABEL] = File(
            trackTempFile, name=trackFileName)
        libraryTrack = TrackService.Create(user=user, postSchemaData=saveData)

    return libraryTrack


def _getSaveDataFromRequestData(requestData: QueryDict):
    saveData = requestData.copy()
    del saveData[MineTrack.ATTRIBUTE_URL_LABEL]
    return saveData


def _getFileExtensionFromUrl(url: str):
    return url.split(".")[-1]


def _getSubstringAfterLastSlash(string: str):
    return string.split("/")[-1]


def _getTrackFileName(mineTrackUrl: str, requestData: QueryDict):
    titleKey = LibraryTrack.ATTRIBUTE_TITLE_LABEL
    if titleKey in requestData:
        title = requestData[titleKey]
        artistNameKey = TrackUpdateSchemaSerializer.ATTRIBUTE_ARTIST_NAME_LABEL
        if artistNameKey in requestData:
            artistName = requestData[artistNameKey]
            if artistName is None or artistName == "":
                fileNameWithoutExtension = title
            else:
                fileNameWithoutExtension = artistName + " - " + title
        else:
            fileNameWithoutExtension = title
    else:
        partAfterLastSlashOfUrl = _getSubstringAfterLastSlash(mineTrackUrl)
        if len(partAfterLastSlashOfUrl) > settings.TRACK_TITLE_MAX_CHAR:
            fileNameWithoutExtension = _generateShortUu(
                settings.TRACK_TITLE_MAX_CHAR)
        else:
            fileNameWithoutExtension = partAfterLastSlashOfUrl
    return fileNameWithoutExtension + "." + _getFileExtensionFromUrl(mineTrackUrl)


def _getTrackTempFileIndividualDirAbsPath():
    trackTempFileIndividualDirName = (
        _generateShortUu(TRACK_TEMP_FILE_INDIVIDUAL_DIR_NAME_LENGTH))
    trackTempFileIndividualDirAbsPath = settings.MEDIA_TEMP + \
        trackTempFileIndividualDirName + "/"
    os.makedirs(trackTempFileIndividualDirAbsPath)
    return trackTempFileIndividualDirAbsPath


def _generateShortUu(length: int):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
