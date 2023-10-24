#!/usr/bin/env python
from  bodzify_api.service.mine.connector import OpenSamplesConnector

def List(baseurl, query, page_number):
    return OpenSamplesConnector.search(baseurl, query, page_number)
