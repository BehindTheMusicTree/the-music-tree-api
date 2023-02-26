#!/usr/bin/env python
import requests
import random
import string
import os
from django.core.files.base import File
from django.http.request import QueryDict
from django.contrib.auth.models import User
from bodzify_api import settings
import bodzify_api.service.TrackService as TrackService
from bodzify_api.model.track.MineTrack import MineTrack
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.criteria.Criteria import CriteriaSpecialNames
import bodzify_api.myfreemp3_scrapper.scrapper as myfreemp3scrapper
from bodzify_api.serializer.track.TrackSaveSchemaSerializer import TrackSaveSchemaSerializer


TRACK_TEMP_FILE_INDIVIDUAL_DIR_NAME_LENGTH = 20


def List(query, pageNumber, pageSize):
    return myfreemp3scrapper.scrap(query, pageNumber, pageSize)


def Extract(user: User, requestData: QueryDict):
    mineTrackUrl = requestData[MineTrack.ATTRIBUTE_URL_LABEL]
    response = requests.get(mineTrackUrl)

    trackTempFileIndividualDirAbsPath = _getTrackTempFileIndividualDirAbsPath()
    trackTempFileName = _getTrackTempFileName(mineTrackUrl, requestData)
    trackTempFileAbsPath = trackTempFileIndividualDirAbsPath + trackTempFileName
    
    
    with open(trackTempFileAbsPath, "wb") as trackFile:
        trackFile.write(response.content)
    
    with open(trackTempFileAbsPath, "rb") as trackFile:
        _validateData(requestData=requestData, trackFile=File(trackFile))

    with open(trackTempFileAbsPath, "rb") as trackFile:
        saveData = requestData.copy()
        saveData[LibraryTrack.ATTRIBUTE_FILE_LABEL] = File(trackFile)
        genreNameKey = TrackSaveSchemaSerializer.ATTRIBUTE_GENRE_NAME_LABEL
        if genreNameKey not in saveData:
            saveData[genreNameKey] = CriteriaSpecialNames.GENRE_GENRELESS
        saveData[LibraryTrack.ATTRIBUTE_FILE_LABEL] = File(trackFile)
        libraryTrack = TrackService.Save(user=user, requestData=saveData)

    os.remove(trackTempFileAbsPath)
    os.rmdir(trackTempFileIndividualDirAbsPath)

    return libraryTrack


def _getFileExtensionFromUrl(url: str):
    return url.split(".")[-1]


def _getTrackTempFileName(mineTrackUrl: str, requestData: QueryDict):
    title = requestData[LibraryTrack.ATTRIBUTE_TITLE_LABEL]
    artistNameKey = TrackSaveSchemaSerializer.ATTRIBUTE_ARTIST_NAME_LABEL
    if artistNameKey in requestData:
        artistName = requestData[artistNameKey]
        if artistName is None or artistName == "":
            fileNameWithoutExtension = title
        else:
            fileNameWithoutExtension = artistName + " - " + title
        return fileNameWithoutExtension + "." + _getFileExtensionFromUrl(mineTrackUrl)


def _getTrackTempFileIndividualDirAbsPath():
    trackTempFileIndividualDirName = (
            _generateShortUu(TRACK_TEMP_FILE_INDIVIDUAL_DIR_NAME_LENGTH))
    trackTempFileIndividualDirAbsPath = settings.MEDIA_TEMP + trackTempFileIndividualDirName + "/"
    os.makedirs(trackTempFileIndividualDirAbsPath)
    return trackTempFileIndividualDirAbsPath
    

def _generateShortUu(length: int):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def _getLastPartOfUrl(url):
    return url.split("/")[-1]


def _validateData(requestData: QueryDict, trackFile: File):
    saveSchemaSerializerData = requestData.copy()
    saveSchemaSerializerData[LibraryTrack.ATTRIBUTE_FILE_LABEL] = File(trackFile)
    saveSchemaSerializerData = requestData.copy()
    saveSchemaSerializer = TrackSaveSchemaSerializer(data=saveSchemaSerializerData)
    saveSchemaSerializer.is_valid(raise_exception=True)
