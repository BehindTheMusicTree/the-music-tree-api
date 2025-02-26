
from enum import Enum

from .AppMetadataKey import AppMetadataKey


class RawMetadataKey(str, Enum):
    pass


"""
Raw metadata value can be none (when not set), string (title), integer (rating), float(BPM) or list[str] (artists 
names).
"""
MetadataValue = list[int] | list[float] | list[str] | None
RawMetadataDict = dict[RawMetadataKey, MetadataValue]
AppMetadataDict = dict[AppMetadataKey, MetadataValue]
