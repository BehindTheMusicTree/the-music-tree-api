#!/usr/bin/env python
from  bodzify_api.service.mine.connector import FreeSampleConnector

def List(baseurl, query, page_number):
    return FreeSampleConnector.search(baseurl, query, page_number)
