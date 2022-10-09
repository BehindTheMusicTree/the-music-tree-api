from datetime import datetime
import os
import os.path
from os import path
import requests
import json

import myfreemp3api.myfreemp3_scrapper.configuration as myfreemp3_cfg
import myfreemp3api.api.configuration as api_cfg
import myfreemp3api.settings as settings

from myfreemp3api.modele.song import Song

def scrap (search):

    dataToSend = {
        'q': search,
        'page':'0'
    }
    
    responseText = requests.post(url = myfreemp3_cfg.configuration["postUrl"], data = dataToSend).text
    logResponseText(responseText)

    myfreemp3songsJsonText = "{" + responseText.split("{",2)[2]
    myfreemp3songsJsonText = myfreemp3songsJsonText[:len(myfreemp3songsJsonText) - 4]
    myfreemp3songsJson = json.loads(myfreemp3songsJsonText)

    songs = getSongsFromMyfreemp3Json(myfreemp3songsJson)
    songsJsonText = getJsonTextFromSongs(songs)
    return json.loads(songsJsonText)

def getSongsFromMyfreemp3Json (dataDict):
    songs = []
    for songJson in dataDict[myfreemp3_cfg.configuration["dataFieldName"]]:
        if songJson != "apple":
            songs.append(Song(
                songJson[myfreemp3_cfg.configuration["titleFieldName"]]
                , songJson[myfreemp3_cfg.configuration["artistFieldName"]]
                , songJson[myfreemp3_cfg.configuration["durationFieldName"]]
                , songJson[myfreemp3_cfg.configuration["dateFieldName"]]
                , songJson[myfreemp3_cfg.configuration["urlFieldName"]]))
    return songs

def logResponseText (responseText):
    myfreemp3ScrapperLogFolderPath = settings.MYFREEMP3_SCRAPPER_LOG_FOLDER_PATH
    
    if not path.exists(myfreemp3ScrapperLogFolderPath):
        os.makedirs(myfreemp3ScrapperLogFolderPath)

    f = open(myfreemp3ScrapperLogFolderPath + datetime.now().strftime("%y-%m-%d %H%M%S") + ".txt", "x")
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
    
