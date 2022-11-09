#!/usr/bin/env python

import requests

from bodzify_api.models import MineTrack
import bodzify_api.myfreemp3_scrapper.scrapper as myfreemp3scrapper
from bodzify_api.dao import LibraryTrackDao

def list(query, pageNumber, pageSize):
    return myfreemp3scrapper.scrap(query, pageNumber, pageSize)

def extract(user, title, artist, duration, releasedOn, mineTrackUrl):
    mineTrack = MineTrack(
        title = title,
        artist = artist,
        duration = duration,
        releasedOn = releasedOn,
        url = mineTrackUrl)

    externalTrackFile = requests.get(mineTrackUrl)
    
    return LibraryTrackDao.createFromMineTrack(mineTrack, externalTrackFile, user)
