
from typing import Dict, Union

from bodzify_api.utils.audio_metadata.AppMetadataKey import AppMetadataKey


TagValue = Union[str, int]
RawMetadataDict = Dict[str, TagValue]
AppMetadataDict = Dict[AppMetadataKey, TagValue]
