#!/usr/bin/env python

import io
import json
import sys

from loader import load

from bodzify_api.model.track.MineTrack import MineTrack


class ResponseFields:
    TITLE = "title"
    ARTIST_NAME = "artistName"
    URL = "url"
    RELEASED_ON = "releasedOn"
    DURATION_IN_SEC = "duration"


def get_samples(baseurl, query, page_number):

    temp_out = io.StringIO()
    sys.stdout = temp_out
    tracks_list_raw = load.get_samples(query, page_number, baseurl)
    sys.stdout = sys.__stdout__

    return get_mine_tracks_from_tracks_list_raw(tracks_list_raw)


def get_mine_tracks_from_tracks_list_raw(tracks_list_raw):
    mine_tracks = []
    data_dict = json.loads(tracks_list_raw)
    for track_raw in data_dict:
        mine_track = MineTrack(title=track_raw[ResponseFields.TITLE],
                               artist_name=track_raw[ResponseFields.ARTIST_NAME],
                               duration_in_sec=track_raw[ResponseFields.DURATION_IN_SEC],
                               released_on=track_raw[ResponseFields.RELEASED_ON],
                               url=track_raw[ResponseFields.URL])
        mine_tracks.append(mine_track)
    return mine_tracks
