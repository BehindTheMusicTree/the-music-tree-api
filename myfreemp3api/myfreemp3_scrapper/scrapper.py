from pickle import FALSE, TRUE
import requests
import string
import json
import configuration as cfg

from myfreemp3api.modele.song import Song

def scrap ():
  
    # data to be sent to api
    data = {
        'q':'Jul',
        'page':'0'
    }
    
    # sending post request and saving response as response object
    responseText = requests.post(url = cfg.configuration["postUrl"], data = data).text
    myfreemp3songsJsonText = "{" + responseText.split("{",2)[2]
    myfreemp3songsJsonText = myfreemp3songsJsonText[:len(myfreemp3songsJsonText) - 4]
    myfreemp3songsJson = json.loads(myfreemp3songsJsonText)

    songs = []

    for songJson in myfreemp3songsJson[cfg.configuration["dataFieldName"]]:
        if songJson != "apple":
            songs.append(Song(
                songJson[cfg.configuration["titleFieldName"]]
                , songJson[cfg.configuration["artistFieldName"]]
                , songJson[cfg.configuration["durationFieldName"]]))

    songsJsonText = "{\"results\": ["
    firstSong = True
    for song in songs:
        if firstSong: firstSong = False
        else: songsJsonText += ", "
        songsJsonText += json.dumps(song.__dict__)
    songsJsonText += "]}"
    print(songsJsonText)
    
    return json.loads(songsJsonText)