
from enum import Enum
from typing import Dict

from .AppMetadataKey import AppMetadataKey


class RawMetadataKey(Enum):
    pass


AppMetadataValue = str | int | float | None
AppMetadataDict = Dict[AppMetadataKey, AppMetadataValue]

"""
Raw metadata value can be string (title), integer (rating), float(BPM) or list[str] (Vorbis).
"""
RawMetadataValue = str | int | float | list[str]
RawMetadataDict = Dict[RawMetadataKey, RawMetadataValue]
