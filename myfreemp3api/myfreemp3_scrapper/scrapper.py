from pickle import FALSE, TRUE
import requests
import json
import myfreemp3api.myfreemp3_scrapper.configuration as myfreemp3_cfg
import myfreemp3api.api.configuration as api_cfg

from myfreemp3api.modele.song import Song

def scrap (search):
  
    # data to be sent to api
    data = {
        'q': search,
        'page':'0'
    }
    
    # sending post request and saving response as response object
    responseText = requests.post(url = myfreemp3_cfg.configuration["postUrl"], data = data).text
    myfreemp3songsJsonText = "{" + responseText.split("{",2)[2]
    myfreemp3songsJsonText = myfreemp3songsJsonText[:len(myfreemp3songsJsonText) - 4]
    myfreemp3songsJson = json.loads(myfreemp3songsJsonText)

    songs = getSongsFromMyfreemp3Json(myfreemp3songsJson)
    songsJsonText = getJsonTextFromSongs(songs)
    return json.loads(songsJsonText)

def getSongsFromMyfreemp3Json (json):
    songs = []
    for songJson in json[myfreemp3_cfg.configuration["dataFieldName"]]:
        if songJson != "apple":
            songs.append(Song(
                songJson[myfreemp3_cfg.configuration["titleFieldName"]]
                , songJson[myfreemp3_cfg.configuration["artistFieldName"]]
                , songJson[myfreemp3_cfg.configuration["durationFieldName"]]
                , songJson[myfreemp3_cfg.configuration["dateFieldName"]]
                , songJson[myfreemp3_cfg.configuration["urlFieldName"]]))
    return songs

def getJsonTextFromSongs (songs):
    songsJsonText = "["
    firstSong = True
    for song in songs:
        if firstSong: firstSong = False
        else: songsJsonText += ", "
        songsJsonText += json.dumps(song.__dict__)
    songsJsonText += "]"
    return songsJsonText
    
