
from typing import Dict, TypedDict, Union

from bodzify_api.utils.audio_metadata.AppMetadataKey import AppMetadataKey


TagValue = Union[str, int]


class RawMetadataDict(TypedDict):
    merged: Dict[str, TagValue]


class AppMetadataDict(TypedDict):
    merged: Dict[AppMetadataKey, TagValue]
