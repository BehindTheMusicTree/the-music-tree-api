#!/usr/bin/env python
import pprint
from free_sample_api import search as free_sample_search
from bodzify_api.model.track.MineTrack import MineTrack

class SEARCH_RESPONSE_FIELDS:
	TITLE = "title"
	ARTIST = "artist"
	URL = "url"
	RELEASED_ON = "date"
	DURATION = "duration"

def search(baseurl, query, page_number):
    tracks_list_raw = free_sample_search.search(baseurl, query, page_number)
    return get_mine_tracks_from_tracks_list_raw(tracks_list_raw)
        
        
def get_mine_tracks_from_tracks_list_raw(tracks_list_raw):
    mine_tracks = []
    for track_raw in tracks_list_raw:
        mine_track = MineTrack(
    		title=track_raw[SEARCH_RESPONSE_FIELDS.TITLE], 
			artist_name=track_raw[SEARCH_RESPONSE_FIELDS.ARTIST],	
			duration=track_raw[SEARCH_RESPONSE_FIELDS.DURATION],	
			released_on=track_raw[SEARCH_RESPONSE_FIELDS.RELEASED_ON],	
			url=track_raw[SEARCH_RESPONSE_FIELDS.URL])
        mine_tracks.append(mine_track)
    return mine_tracks