#!/usr/bin/env python

from bodzify_api.service.mine.connector import open_samples


def List(baseurl, query, page_number):
    return open_samples.get_samples(baseurl, query, page_number)
