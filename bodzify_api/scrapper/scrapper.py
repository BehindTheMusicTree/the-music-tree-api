import datetime
import os
import requests
import json

from bodzify_api.model.track.MineTrack import MineTrack

import bodzify_api.settings as settings


LOG_SCRAPPER_FOLDER_PATH = os.path.join(settings.LOG_PATH, "scrapper/")
LOG_FILE_NAME_FORMAT = "%y-%m-%d %H%M%S"

POST_URL_BASE = 'https://new.myfreemp3juices.cc/api/'
POST_URL_SEARCH_PHP_PARAMETER = 'search.php?callback=jQuery2130710897661425719_1686994670460'
POST_URL_SEARCH_JSON_PARAMETER = 'search.json?page={}&page_size={}&search_term=a'
POST_URL = POST_URL_BASE + POST_URL_SEARCH_PHP_PARAMETER + POST_URL_SEARCH_JSON_PARAMETER

DATA_FIELD = "response"
TITLE_FIELD = "title"
ARTIST_FIELD = "artist"
URL_FIELD = "url"
RELEASED_ON_FIELD = "date"
DURATION_FIELD = "duration"

QUERY_FIELD = "q"
PAGE_FIELD = "page"
PAGE_SIZE_FIELD = "page_size"

TAG_TO_IGNORE = "apple"


def Scrap(search, page, pageSize):
    dataToSendToScrappedWebsite = {
        QUERY_FIELD: search,
        PAGE_FIELD: str(page)
    }

    responseIsInvalid = True
    while responseIsInvalid:
        response = requests.post(url = POST_URL, data = dataToSendToScrappedWebsite)
        if response.status_code != 200:
            raise Exception("Error while scrapping: " + response.reason)
        responseText = response.text
        responseIsInvalid = _isResponseTextIsValid(responseText)
    
    responseTracksJson = _getResponseJsonFromResponseText(response.text)        
    tracks = _getTracksFromResponseJson(responseTracksJson)
    tracksJsonText = _getJsonTextFromTracks(tracks)
    return json.loads(tracksJsonText)


def _getTracksFromResponseJson(dataDict):
    tracks = []
    for trackJson in dataDict[DATA_FIELD]:
        if trackJson != TAG_TO_IGNORE:
            tracks.append(MineTrack(
                title=trackJson[TITLE_FIELD], 
                artistName=trackJson[ARTIST_FIELD], 
                duration=trackJson[DURATION_FIELD], 
                releasedOn=trackJson[RELEASED_ON_FIELD],
                url=trackJson[URL_FIELD]))
    return tracks


def _getJsonTextFromTracks(tracks):
    tracksJsonText = "["
    firstTrack = True
    for track in tracks:
        if firstTrack: firstTrack = False
        else: tracksJsonText += ", "
        tracksJsonText += json.dumps(track.__dict__)
    tracksJsonText += "]"
    return tracksJsonText


def _getResponseJsonFromResponseText(responseJsonResponseText):
    responseTracksJsonText = "{" + responseJsonResponseText.split("{",2)[2]
    responseTracksJsonText = responseTracksJsonText[:len(responseTracksJsonText) - 4]
    return json.loads(responseTracksJsonText)


def _getFirstStringBetweenTwoStrings(string, string1, string2):
    return string.split(string1,1)[1].split(string2,1)[0]


def _isResponseTextIsValid(responseText):
    print("REEEESPOOOONSE")
    print(responseText)
    print(_getFirstStringBetweenTwoStrings(responseText, "response\":", "});"))
    return _getFirstStringBetweenTwoStrings(responseText, "response\":", "});") == "null"