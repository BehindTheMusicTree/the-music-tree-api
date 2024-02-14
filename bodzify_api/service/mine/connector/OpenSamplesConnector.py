#!/usr/bin/env python
import json
from loader import load
from bodzify_api.model.track.MineTrack import MineTrack

class SEARCH_RESPONSE_FIELDS:
	TITLE = "title"
	ARTIST_NAME = "artist_name"
	URL = "url"
	RELEASED_ON = "releasedOn"
	DURATION = "duration"


def search(baseurl, query, page_number):
    tracks_list_raw = load.get_samples(query, page_number, baseurl)
    return get_mine_tracks_from_tracks_list_raw(tracks_list_raw)
        
        
def get_mine_tracks_from_tracks_list_raw(tracks_list_raw):
	mine_tracks = []
	data_dict = json.loads(tracks_list_raw)
	for track_raw in data_dict:
		mine_track = MineTrack(
			title=track_raw[SEARCH_RESPONSE_FIELDS.TITLE], 
			artist_name=track_raw[SEARCH_RESPONSE_FIELDS.ARTIST_NAME],    
			duration=track_raw[SEARCH_RESPONSE_FIELDS.DURATION],    
			released_on=track_raw[SEARCH_RESPONSE_FIELDS.RELEASED_ON],    
			url=track_raw[SEARCH_RESPONSE_FIELDS.URL])
		mine_tracks.append(mine_track)
	return mine_tracks
