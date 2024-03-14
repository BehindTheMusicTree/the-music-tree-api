#!/usr/bin/env python

import pytest
from ddf import G
from rest_framework import status
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.test import conftest
from bodzify_api.test.view.playlist.mother.get.TestCase import TestCase


@pytest.fixture(params=[TestCase])
def child_instance(request, db):
    yield from conftest.base_child_instance(request, db)
