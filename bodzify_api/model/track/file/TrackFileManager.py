#!/usr/bin/env python

from typing import TYPE_CHECKING
from django.db import models

if TYPE_CHECKING:
    from bodzify_api.model.track.file.TrackFile import TrackFile

class TrackFileManager(models.Manager['TrackFile']:
    
