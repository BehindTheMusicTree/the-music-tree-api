#!/usr/bin/env python
from  bodzify_api.service.mine.connector import FreeSampleConnector

def List(baseUrl, query, pageNumber):
    return FreeSampleConnector.search(baseUrl, query, pageNumber)
