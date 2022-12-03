import datetime
import os
import requests
import json

from bodzify_api.model.track.MineTrack import MineTrack

import bodzify_api.settings as settings


LOG_FOLDER_PATH = os.path.join(settings.LOG_PATH, "myfreemp3Scrapper/")
LOG_FILE_NAME_FORMAT = "%y-%m-%d %H%M%S"

POST_URL_BASE = 'https://myfreemp3juices.cc/api/'
POST_URL_SEARCH_PHP_PARAMETER = 'search.php?callback=jQuery21307552220673040206_1662375436837'
POST_URL_SEARCH_JSON_PARAMETER = 'search.json?page={}&page_size={}&search_term=a'
POST_URL = POST_URL_BASE + POST_URL_SEARCH_PHP_PARAMETER + POST_URL_SEARCH_JSON_PARAMETER
FIELD_DATA = "response"
FIELD_TITLE = "title"
FIELD_ARTIST = "artist"
FIELD_URL = "url"
FIELD_RELEASED_ON = "date"
FIELD_DURATION = "duration"

QUERY_FIELD = "q"
PAGE_FIELD = "page"
PAGE_SIZE_FIELD = "page_size"

TAG_TO_IGNORE = "apple"


def getTracksFromMyfreemp3Json(dataDict):
    tracks = []
    for trackJson in dataDict[FIELD_DATA]:
        if trackJson != TAG_TO_IGNORE:
            tracks.append(MineTrack(
                title=trackJson[FIELD_TITLE], 
                artist=trackJson[FIELD_ARTIST], 
                duration=trackJson[FIELD_DURATION], 
                releasedOn=trackJson[FIELD_RELEASED_ON],
                url=trackJson[FIELD_URL]))
    return tracks


def logResponseText(responseText):
    myfreemp3ScrapperLogFolderPath = LOG_FOLDER_PATH
    
    if not os.path.exists(myfreemp3ScrapperLogFolderPath):
        os.makedirs(myfreemp3ScrapperLogFolderPath)

    logFileName = datetime.datetime.now().strftime(LOG_FILE_NAME_FORMAT) + ".txt"
    f = open(LOG_FOLDER_PATH + logFileName, "x")
    f.write(responseText)
    f.close()


def getJsonTextFromTracks(tracks):
    tracksJsonText = "["
    firstTrack = True
    for track in tracks:
        if firstTrack: firstTrack = False
        else: tracksJsonText += ", "
        tracksJsonText += json.dumps(track.__dict__)
    tracksJsonText += "]"
    return tracksJsonText


def getMyfreemp3ResponseJsonFromMyfreemp3ResponseText(myfreemp3ResponseJsonResponseText):
    myfreemp3tracksJsonText = "{" + myfreemp3ResponseJsonResponseText.split("{",2)[2]
    myfreemp3tracksJsonText = myfreemp3tracksJsonText[:len(myfreemp3tracksJsonText) - 4]
    return json.loads(myfreemp3tracksJsonText)


def scrap(search, page, pageSize):
    dataToSendToMyfreemp3 = {
        QUERY_FIELD: search,
        PAGE_FIELD: str(page)
    }
    
    responseText = requests.post(url = POST_URL, data = dataToSendToMyfreemp3).text
    logResponseText(responseText)

    myfreemp3tracksJson = getMyfreemp3ResponseJsonFromMyfreemp3ResponseText(responseText)
    tracks = getTracksFromMyfreemp3Json(myfreemp3tracksJson)
    tracksJsonText = getJsonTextFromTracks(tracks)
    return json.loads(tracksJsonText)
    
