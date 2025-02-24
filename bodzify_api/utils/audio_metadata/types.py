
from typing import Dict

from bodzify_api.utils.audio_metadata.AppMetadataKey import AppMetadataKey


MetadataValue = str | int | float
RawMetadataDict = Dict[str, MetadataValue]
AppMetadataDict = Dict[AppMetadataKey, MetadataValue]
