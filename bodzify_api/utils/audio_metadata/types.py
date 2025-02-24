
from enum import Enum
from typing import Dict

from .AppMetadataKey import AppMetadataKey


class RawMetadataKey(Enum):
    pass


AppMetadataValue = str | int | float

"""
Raw metadata value can be string (title), integer (rating), float(BPM) or lists (Vorbis).
"""
RawMetadataValue = str | int | float | list
RawMetadataDict = Dict[RawMetadataKey, RawMetadataValue]
AppMetadataDict = Dict[AppMetadataKey, AppMetadataValue]
