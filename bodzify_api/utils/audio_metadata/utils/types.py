
from enum import Enum


from .AppMetadataKey import AppMetadataKey


class RawMetadataKey(Enum):
    pass


AppMetadataValue = str | int | float | None
AppMetadataDict = dict[AppMetadataKey, AppMetadataValue]

"""
Raw metadata value can be string (title), integer (rating), float(BPM) or list[str] (Vorbis).
"""
RawMetadataValue = str | int | float | list[str]
RawMetadataDict = dict[RawMetadataKey, RawMetadataValue]
