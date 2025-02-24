
from enum import Enum
from typing import Dict

from .AppMetadataKey import AppMetadataKey


class RawMetadataKey(Enum):
    pass


MetadataValue = str | int | float
RawMetadataDict = Dict[RawMetadataKey, MetadataValue]
AppMetadataDict = Dict[AppMetadataKey, MetadataValue]
