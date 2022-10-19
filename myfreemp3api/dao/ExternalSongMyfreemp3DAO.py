#!/usr/bin/env python

import myfreemp3api.myfreemp3scrapper.scrapper as myfreemp3scrapper

class ExternalSongMyfreemp3DAO:
    def get_list(query, pageNumber):
        return myfreemp3scrapper.scrap(query, pageNumber)
