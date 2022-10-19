import datetime
import os
import requests
import json

import myfreemp3api.myfreemp3scrapper.settings as myfreemp3Settings

from myfreemp3api.models import ExternalSong

def getSongsFromMyfreemp3Json (dataDict):
    songs = []
    for songJson in dataDict[myfreemp3Settings.FIELD_DATA]:
        if songJson != "apple":
            songs.append(ExternalSong(
                songJson[myfreemp3Settings.FIELD_TITLE]
                , songJson[myfreemp3Settings.FIELD_ARTIST]
                , songJson[myfreemp3Settings.FIELD_DURATION]
                , songJson[myfreemp3Settings.FIELD_DATE]
                , songJson[myfreemp3Settings.FIELD_URL]))
    return songs

def logResponseText (responseText):
    myfreemp3ScrapperLogFolderPath = myfreemp3Settings.LOG_FOLDER_PATH
    
    if not os.path.exists(myfreemp3ScrapperLogFolderPath):
        os.makedirs(myfreemp3ScrapperLogFolderPath)

    logFileName = datetime.datetime.now().strftime(myfreemp3Settings.LOG_FILE_NAME_FORMAT) + ".txt"
    f = open(myfreemp3Settings.LOG_FOLDER_PATH + logFileName, "x")
    f.write(responseText)
    f.close()

def getJsonTextFromSongs (songs):
    songsJsonText = "["
    firstSong = True
    for song in songs:
        if firstSong: firstSong = False
        else: songsJsonText += ", "
        songsJsonText += json.dumps(song.__dict__)
    songsJsonText += "]"
    return songsJsonText

def getMyfreemp3ResponseJsonFromMyfreemp3ResponseText (myfreemp3ResponseJsonResponseText):
    myfreemp3songsJsonText = "{" + myfreemp3ResponseJsonResponseText.split("{",2)[2]
    myfreemp3songsJsonText = myfreemp3songsJsonText[:len(myfreemp3songsJsonText) - 4]
    return json.loads(myfreemp3songsJsonText)

def scrap (search, page):

    dataToSendToMyfreemp3 = {
        'q': search,
        'page': str(page)
    }
    
    responseText = requests.post(url = myfreemp3Settings.POST_URL, data = dataToSendToMyfreemp3).text
    logResponseText(responseText)

    myfreemp3songsJson = getMyfreemp3ResponseJsonFromMyfreemp3ResponseText(responseText)
    songs = getSongsFromMyfreemp3Json(myfreemp3songsJson)
    songsJsonText = getJsonTextFromSongs(songs)
    return json.loads(songsJsonText)
    
