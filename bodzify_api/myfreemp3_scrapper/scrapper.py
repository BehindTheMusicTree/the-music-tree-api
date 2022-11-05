import datetime
import os
import requests
import json

import bodzify_api.myfreemp3_scrapper.settings as myfreemp3ScrapperSettings
from bodzify_api.models import MineTrack

def getTracksFromMyfreemp3Json (dataDict):
    tracks = []
    for trackJson in dataDict[myfreemp3ScrapperSettings.FIELD_DATA]:
        if trackJson != "apple":
            tracks.append(MineTrack(
                title=trackJson[myfreemp3ScrapperSettings.FIELD_TITLE], 
                artist=trackJson[myfreemp3ScrapperSettings.FIELD_ARTIST], 
                duration=trackJson[myfreemp3ScrapperSettings.FIELD_DURATION], 
                releasedOn=trackJson[myfreemp3ScrapperSettings.FIELD_RELEASED_ON],
                url=trackJson[myfreemp3ScrapperSettings.FIELD_URL]))
    return tracks

def logResponseText (responseText):
    myfreemp3ScrapperLogFolderPath = myfreemp3ScrapperSettings.LOG_FOLDER_PATH
    
    if not os.path.exists(myfreemp3ScrapperLogFolderPath):
        os.makedirs(myfreemp3ScrapperLogFolderPath)

    logFileName = datetime.datetime.now().strftime(myfreemp3ScrapperSettings.LOG_FILE_NAME_FORMAT) + ".txt"
    f = open(myfreemp3ScrapperSettings.LOG_FOLDER_PATH + logFileName, "x")
    f.write(responseText)
    f.close()

def getJsonTextFromTracks (tracks):
    tracksJsonText = "["
    firstTrack = True
    for track in tracks:
        if firstTrack: firstTrack = False
        else: tracksJsonText += ", "
        tracksJsonText += json.dumps(track.__dict__)
    tracksJsonText += "]"
    return tracksJsonText

def getMyfreemp3ResponseJsonFromMyfreemp3ResponseText (myfreemp3ResponseJsonResponseText):
    myfreemp3tracksJsonText = "{" + myfreemp3ResponseJsonResponseText.split("{",2)[2]
    myfreemp3tracksJsonText = myfreemp3tracksJsonText[:len(myfreemp3tracksJsonText) - 4]
    return json.loads(myfreemp3tracksJsonText)

def scrap (search, page):

    dataToSendToMyfreemp3 = {
        'q': search,
        'page': str(page)
    }
    
    responseText = requests.post(url = myfreemp3ScrapperSettings.POST_URL, data = dataToSendToMyfreemp3).text
    logResponseText(responseText)

    myfreemp3tracksJson = getMyfreemp3ResponseJsonFromMyfreemp3ResponseText(responseText)
    tracks = getTracksFromMyfreemp3Json(myfreemp3tracksJson)
    tracksJsonText = getJsonTextFromTracks(tracks)
    return json.loads(tracksJsonText)
    
