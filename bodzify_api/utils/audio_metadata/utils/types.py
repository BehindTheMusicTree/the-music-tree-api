
from enum import Enum

from .AppMetadataKey import AppMetadataKey


class RawMetadataKey(str, Enum):
    pass


"""
Raw metadata value can be none (when not set), string (title), integer (rating), float(BPM) or list[str] (artists 
names).
"""
AppMetadataValue = int | float | str | list[str] | None
RawMetadataValue = list[int] | list[float] | list[str] | None
RawMetadataDict = dict[RawMetadataKey, RawMetadataValue]
AppMetadataDict = dict[AppMetadataKey, AppMetadataValue]
