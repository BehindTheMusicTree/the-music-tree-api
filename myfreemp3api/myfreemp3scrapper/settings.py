#!/usr/bin/env python

import myfreemp3api.settings as myfreemp3settings
import os

LOG_FOLDER_PATH = os.path.join(myfreemp3settings.LOG_PATH, "myfreemp3Scrapper/")
LOG_FILE_NAME_FORMAT = "%y-%m-%d %H%M%S"

POST_URL = 'https://myfreemp3juices.cc/api/search.php?callback=jQuery21307552220673040206_1662375436837' + 'search.json?page={}&page_size={}&search_term=a'
FIELD_DATA = "response"
FIELD_TITLE = "title"
FIELD_ARTIST = "artist"
FIELD_URL = "url"
FIELD_RELEASED_ON = "date"
FIELD_DURATION = "duration"