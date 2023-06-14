#!/usr/bin/env python

import bodzify_api.myfreemp3_scrapper.scrapper as myfreemp3scrapper


def List(query, pageNumber, pageSize):
    return myfreemp3scrapper.Scrap(query, pageNumber, pageSize)
