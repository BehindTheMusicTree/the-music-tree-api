#!/usr/bin/env python

from importlib import metadata
import os
import subprocess
from typing import Optional

from .id3.Id3Manager import Id3Manager
from .id3.Mp3MetadataManager import Mp3MetadataManager
from .id3.WavMetadataManager import WavMetadataManager
from .vorbis.VorbisManager import VorbisManager
from .MetadataManager import NormalizedMetadataKeys, MetadataManager, METADATA_ARTISTS_SEPARATION_CHAR


# def get_specific_metadata_from_file(file, metadata_key: str):
#     _, file_extension = os.path.splitext(file.name)
#     file_extension_lowered = file_extension.lower()
#     if file_extension_lowered in [".wav", ".mp3"]:
#         file_tags = MutagenFile(file)
#         return get_specific_file_metadata_from_id3_file(file_metadata=file_tags, metadata_key=metadata_key)
#     elif file_extension_lowered == ".flac":
#         flac_metadata = _get_metadata(file)
#         return get_specific_file_metadata_from_flac_file(flac_metadata=flac_metadata, metadata_key=metadata_key)
#     else:
#         raise ValueError(FILE_EXTENSION_NOT_HANDLED_MESSAGE)

FILE_EXTENSION_NOT_HANDLED_MESSAGE = "The file's format is not handled by the service."


def get_specific_metadata_from_file(file, normalized_metadata_key: str):
    return _get_metadata_manager(file).get_specific_file_metadata(normalized_metadata_key=normalized_metadata_key)


def get_normalized_metadata_from_file(file, normalized_rating_max_value: Optional[int] = None) -> dict:

    metadata_manager = _get_metadata_manager(file)

    metadata_dict = dict()
    metadata_dict[NormalizedMetadataKeys.TITLE] = metadata_manager.get_title()
    metadata_dict[NormalizedMetadataKeys.ARTIST_NAME] = metadata_manager.get_artist_name()
    metadata_dict[NormalizedMetadataKeys.ALBUM_NAME] = metadata_manager.get_album_name()
    metadata_dict[NormalizedMetadataKeys.ALBUM_ARTISTS_NAMES] = metadata_manager.get_album_artists_name_str()
    metadata_dict[NormalizedMetadataKeys.GENRE_NAME] = metadata_manager.get_genre_name()
    metadata_dict[NormalizedMetadataKeys.DURATION] = metadata_manager.get_duration()
    metadata_dict[NormalizedMetadataKeys.RATING] = metadata_manager.get_eventually_normalized_rating_value(
        normalized_rating_max_value=normalized_rating_max_value)
    metadata_dict[NormalizedMetadataKeys.LANGUAGE] = metadata_manager.get_language()
    return metadata_dict


def _get_metadata_manager(file) -> MetadataManager:
    _, file_extension = os.path.splitext(file.name)
    file_extension_lowered = file_extension.lower()
    if file_extension_lowered == ".mp3":
        return Mp3MetadataManager(file)
    elif file_extension_lowered == ".wav":
        return WavMetadataManager(file)
    elif file_extension_lowered == ".flac":
        return VorbisManager(file)
    else:
        raise ValueError(FILE_EXTENSION_NOT_HANDLED_MESSAGE)


def update_file_metadata(file, normalized_metadata: dict, normalized_rating_max_value: int):
    _get_metadata_manager(file).update_file_metadata(normalized_metadata=normalized_metadata,
                                                     normalized_rating_max_value=normalized_rating_max_value)


def is_flac_file_md5_valid(file_path):
    result = subprocess.run(['flac', '-t', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return 'ok' in result.stderr.decode()


def replace_flac_file_with_corrected_md5(file_path):
    result = subprocess.run(['flac', '-f', '--best', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stderr = result.stderr.decode()
    if 'wrote' not in stderr:
        raise Exception("The Flac file md5 check failed and could not be corrected. The file is probably corrupted.")
