
from typing import Dict, Union

from bodzify_api.utils.audio_metadata.AppMetadataKey import AppMetadataKey


MetadataValue = Union[str, int]
RawMetadataDict = Dict[str, MetadataValue]
AppMetadataDict = Dict[AppMetadataKey, MetadataValue]
