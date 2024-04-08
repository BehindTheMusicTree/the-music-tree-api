#!/usr/bin/env python

import io
import os
from typing import Optional
from tinytag import TinyTag
import tempfile

from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from mutagen._file import File as MutagenFile
from mutagen.flac import FLAC
from mutagen.id3 import ID3
from mutagen.id3._frames import POPM, TALB, TCON, TIT2, TLAN, TPE1, TPE2
from mutagen.id3._util import ID3NoHeaderError
from mutagen.wave import WAVE
from django.db.models.fields.files import FieldFile
from mutagen.mp3 import MP3

TAG_ARTISTS_SEPARATION_CHAR = ","

BASE_255_RATING_STAR_VALUES = [0, 13, 1, 54, 64, 118, 128, 186, 196, 242, 255]
BASE_255_PROPORTIONAL_RATING_STAR_VALUES = [None, None, 51, None, 102, None, 153, None, 204, None, 255]
BASE_100_RATING_STAR_VALUES = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

TRAKTOR_RATING_TAG_MAIL = 'traktor@native-instruments.de'

FILE_EXTENSION_NOT_HANDLED_MESSAGE = "The file's format is not handled by the service."
METADATA_DICT_UPDATE_DURATION_SHOULDNT_BE_SET_MESSAGE = """The duration key has a value in the
metadata dict. The duration cannot be updated. It is therefore ignored."""
METADATA_DICT_UPDATE_KEY_NOT_HANDLED_MESSAGE = """The specified audio metadata key is not
handled by the service."""


class ID3_TEXT_FRAMES:  # MP3 and Wave (.wav) files use ID3 tags
    TITLE = 'TIT2'
    ARTIST_NAME = 'TPE1'
    ALBUM_NAME = 'TALB'
    ALBUM_ARTISTS_NAMES = 'TPE2'
    GENRE_NAME = 'TCON'
    RATING = 'POPM'
    LANGUAGE = 'TLAN'


ID3_RATING_APP_EMAIL = 'bodzify'


class VORBIS_TAG_KEYS:  # FLAC files use Vorbis tags
    TITLE = 'title'
    ARTIST_NAME = 'artist'
    ALBUM_NAME = 'album'
    ALBUM_ARTISTS_NAMES = 'albumartist'
    GENRE_NAME = 'genre'
    RATING = 'rating'
    RATING_TRAKTOR = 'rating wmp'
    LANGUAGE = 'language'


class METADATA_DICT_KEYS:
    TITLE = 'title'
    ARTIST_NAME = 'artist_name'
    ALBUM_NAME = 'album_name'
    ALBUM_ARTISTS_NAMES = 'album_artists_names_string'
    GENRE_NAME = 'genre_name'
    DURATION = 'duration'
    RATING = 'rating'
    LANGUAGE = 'language'


class RATING_FILE_PROFILE:
    BASE_255 = '255'
    BASE_100 = '100'


def get_metadata_dict_from_file(file, normalized_rating_max_value: Optional[int] = None) -> dict:
    filename, file_extension = os.path.splitext(file.name)

    title = ""
    artist_name = ""
    album_name = ""
    album_artists_name_string = ""
    genre_name = ""
    rating = None
    language = ""

    file_extension_lowered = file_extension.lower()
    if file_extension_lowered in [".wav", ".mp3"]:
        if file_extension_lowered == ".mp3":
            file_tags = _get_tags_from_mp3_file(file)
        else:
            file_tags = MutagenFile(file)
        title = _get_title_tag_from_id3_file_tags(file_tags)
        artist_name = _get_artist_name_tag_from_id3_file_tags(file_tags)
        album_name = _get_album_name_tag_from_id3_file_tags(file_tags)
        album_artists_name_string = _get_album_artists_name_str_tag_from_id3_file_tags(file_tags)
        genre_name = _get_genre_name_tag_from_id3_file_tags(file_tags)
        rating = _get_eventually_normalized_rating_value_from_id3_file_tags(file_tags, normalized_rating_max_value)
        language = _get_language_tag_from_id3_file_tags(file_tags)

    elif file_extension.lower() == ".flac":
        file_tags = _create_flac_object_dealing_with_eventual_temporary_file(file)
        title = _get_title_tag_from_flac_file_tags(file_tags)
        artist_name = _get_artist_name_tagFrom_flac_file_tags(file_tags)
        album_name = _get_album_name_tagFrom_flac_file_tags(file_tags)
        album_artists_name_string = _get_album_artists_nametring_tagFrom_flac_file_tags(file_tags)
        genre_name = _get_genre_name_tag_from_flac_file_tags(file_tags)
        rating = _get_eventually_normalized_rating_value_from_flac_file_tags(file_tags, normalized_rating_max_value)
        language = _get_language_tag_from_flac_file_tags(file_tags)
    else:
        raise ValueError(FILE_EXTENSION_NOT_HANDLED_MESSAGE)

    metadata_dict = dict()
    metadata_dict[METADATA_DICT_KEYS.TITLE] = title
    metadata_dict[METADATA_DICT_KEYS.ARTIST_NAME] = artist_name
    metadata_dict[METADATA_DICT_KEYS.ALBUM_NAME] = album_name
    metadata_dict[METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES] = album_artists_name_string
    metadata_dict[METADATA_DICT_KEYS.GENRE_NAME] = genre_name
    duration = _get_duration_from_file_tags(file_tags=file_tags)
    if duration is None:
        duration = _get_duration_from_file_using_TinyTag(file)
    metadata_dict[METADATA_DICT_KEYS.DURATION] = duration
    metadata_dict[METADATA_DICT_KEYS.RATING] = rating
    metadata_dict[METADATA_DICT_KEYS.LANGUAGE] = language
    return metadata_dict


def _get_duration_from_file_using_TinyTag(file):
    if isinstance(file, TemporaryUploadedFile):
        with open(file.temporary_file_path(), 'rb') as f:
            return TinyTag.get(f.name).duration
    elif isinstance(file, FieldFile):
        with open(file.path, 'rb') as f:
            return TinyTag.get(f.name).duration
    elif isinstance(file, InMemoryUploadedFile):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            for chunk in file.chunks():
                tmp.write(chunk)
            return TinyTag.get(tmp.name).duration
    return TinyTag.get(file.name).duration


def _get_tags_from_mp3_file(file):
    if isinstance(file, InMemoryUploadedFile):
        try:
            return MutagenFile(file)
        except ID3NoHeaderError:
            return ID3()
    else:
        return MP3(file).tags


def update(file, metadata_update_dict: dict, normalized_rating_max_value: int):
    filename, file_extension = os.path.splitext(file.name)
    file_extension_lowered = file_extension.lower()

    if file_extension_lowered in [".wav", ".mp3"]:
        if file_extension_lowered == ".mp3":
            file_tags = _get_tags_from_mp3_file(file)
        if file_extension_lowered == ".wav":
            mutagen_wave_file = WAVE()
            mutagen_wave_file.add_tags()
            file_tags = mutagen_wave_file.tags
        for metadata_dict_key in list(metadata_update_dict.keys()):
            if metadata_dict_key == METADATA_DICT_KEYS.DURATION:
                raise ValueError(
                    METADATA_DICT_UPDATE_DURATION_SHOULDNT_BE_SET_MESSAGE)
            else:
                file_tags = _get_id3_file_tags_updated_with_metadata_value(
                    id3_file_tags=file_tags,
                    update_metadata_dict=metadata_update_dict,
                    update_metadata_key=metadata_dict_key,
                    normalized_rating_max_value=normalized_rating_max_value)
    elif file_extension_lowered == ".flac":
        file_tags = _create_flac_object_dealing_with_eventual_temporary_file(
            file)
        for metadata_dict_key in list(metadata_update_dict.keys()):
            if metadata_dict_key == METADATA_DICT_KEYS.DURATION:
                raise ValueError(
                    METADATA_DICT_UPDATE_DURATION_SHOULDNT_BE_SET_MESSAGE)
            else:
                file_tags = _get_flac_file_tags_updated_if_value_specified(
                    flac_file_tags=file_tags,
                    metadata_update_dict=metadata_update_dict,
                    metadata_dictKey=metadata_dict_key,
                    normalized_rating_max_value=normalized_rating_max_value)
    else:
        raise ValueError(FILE_EXTENSION_NOT_HANDLED_MESSAGE)
    file_tags.save(file.path)


def get_specific_metadata_from_file(file, metadata_key: str):
    filename, file_extension = os.path.splitext(file.name)
    file_extension_lowered = file_extension.lower()
    if file_extension_lowered in [".wav", ".mp3"]:
        file_tags = MutagenFile(file)
        return _get_specific_metadata_from_id3_file(id3_file_tags=file_tags, metadata_key=metadata_key)
    elif file_extension_lowered == ".flac":
        flac_file_tags = _create_flac_object_dealing_with_eventual_temporary_file(file)
        return _get_specific_metadata_from_flac_file(flac_file_tags=flac_file_tags, metadata_key=metadata_key)
    else:
        raise ValueError(FILE_EXTENSION_NOT_HANDLED_MESSAGE)


def _create_flac_object_dealing_with_eventual_temporary_file(file):
    if isinstance(file, TemporaryUploadedFile):
        with open(file.temporary_file_path(), 'rb') as f:
            return FLAC(fileobj=io.BytesIO(f.read()))
    elif isinstance(file, FieldFile):
        with open(file.path, 'rb') as f:
            return FLAC(fileobj=f)
    elif isinstance(file, InMemoryUploadedFile):
        file.seek(0)
        return FLAC(io.BytesIO(file.read()))
    return FLAC(fileobj=file)


def _get_duration_from_file_tags(file_tags):
    if hasattr(file_tags, 'info'):
        return file_tags.info.length
    return None


def _get_title_tag_from_id3_file_tags(id3_file_tags: MutagenFile):
    return _get_first_value_if_exists_or_none(id3_file_tags, ID3_TEXT_FRAMES.TITLE)


def _get_artist_name_tag_from_id3_file_tags(id3_file_tags: MutagenFile):
    return _get_first_value_if_exists_or_none(id3_file_tags, ID3_TEXT_FRAMES.ARTIST_NAME)


def _get_album_name_tag_from_id3_file_tags(id3_file_tags: MutagenFile):
    return _get_first_value_if_exists_or_none(id3_file_tags, ID3_TEXT_FRAMES.ALBUM_NAME)


def _get_album_artists_name_str_tag_from_id3_file_tags(id3_file_tags: MutagenFile):
    album_artists_name_stringRaw = (
        _get_first_value_if_exists_or_none(id3_file_tags, ID3_TEXT_FRAMES.ALBUM_ARTISTS_NAMES))
    if album_artists_name_stringRaw is not None:
        return album_artists_name_stringRaw.strip()
    return None


def _get_genre_name_tag_from_id3_file_tags(id3_file_tags: MutagenFile):
    if ID3_TEXT_FRAMES.GENRE_NAME in id3_file_tags:
        return id3_file_tags[ID3_TEXT_FRAMES.GENRE_NAME][0]
    else:
        return ""


def _get_eventually_normalized_rating_from_file_value(
        file_rating_value: int,
        normalized_rating_max_value: Optional[int] = None,
        is_rating_from_traktor: bool = False):
    if file_rating_value is not None:
        if normalized_rating_max_value is not None:
            if file_rating_value == 0 and is_rating_from_traktor:
                return None
            for star_rating_base_10 in range(11):
                if file_rating_value in [
                        BASE_255_RATING_STAR_VALUES[star_rating_base_10],
                        BASE_255_PROPORTIONAL_RATING_STAR_VALUES[star_rating_base_10],
                        BASE_100_RATING_STAR_VALUES[star_rating_base_10]]:
                    return int(star_rating_base_10 * normalized_rating_max_value / 10)
            raise ValueError("Rating value not handled: " + str(file_rating_value))
        else:
            return file_rating_value
    else:
        return None


def _get_eventually_normalized_rating_value_from_id3_file_tags(
        id3_file_tags: MutagenFile, normalized_rating_max_value: Optional[int] = None):
    file_rating_value = None
    for key in id3_file_tags:
        if ID3_TEXT_FRAMES.RATING in key:
            file_rating_tag = id3_file_tags[key]
            file_rating_email = file_rating_tag.email
            file_rating_value = file_rating_tag.rating
    if file_rating_value is None:
        return None
    else:
        return _get_eventually_normalized_rating_from_file_value(
            file_rating_value=file_rating_value,
            is_rating_from_traktor=(file_rating_email == TRAKTOR_RATING_TAG_MAIL),
            normalized_rating_max_value=normalized_rating_max_value)


def _get_eventually_normalized_rating_value_from_flac_file_tags(
        flac_file_tags: FLAC, normalized_rating_max_value: Optional[int] = None):
    file_rating = _get_first_value_int_if_exists_or_none(dict=flac_file_tags, key=VORBIS_TAG_KEYS.RATING)
    is_rating_from_traktor = False
    if file_rating is None:
        file_rating = _get_first_value_int_if_exists_or_none(dict=flac_file_tags, key=VORBIS_TAG_KEYS.RATING_TRAKTOR)
        if file_rating is not None:
            is_rating_from_traktor = True

    if file_rating is None or file_rating == "":
        return None
    else:
        return _get_eventually_normalized_rating_from_file_value(
            file_rating_value=file_rating,
            is_rating_from_traktor=is_rating_from_traktor,
            normalized_rating_max_value=normalized_rating_max_value)


def _get_language_tag_from_id3_file_tags(id3_file_tags: MutagenFile):
    return _get_first_value_if_exists_or_none(id3_file_tags, ID3_TEXT_FRAMES.LANGUAGE)


def _get_title_tag_from_flac_file_tags(flac_file_tags: FLAC):
    return _get_first_value_if_exists_or_none(flac_file_tags, VORBIS_TAG_KEYS.TITLE)


def _get_artist_name_tagFrom_flac_file_tags(flac_file_tags: FLAC):
    return _get_first_value_if_exists_or_none(flac_file_tags, VORBIS_TAG_KEYS.ARTIST_NAME)


def _get_album_name_tagFrom_flac_file_tags(flac_file_tags: FLAC):
    return _get_first_value_if_exists_or_none(flac_file_tags, VORBIS_TAG_KEYS.ALBUM_NAME)


def _get_album_artists_nametring_tagFrom_flac_file_tags(flac_file_tags: FLAC):
    album_artists_name_stringRaw = (
        _get_first_value_if_exists_or_none(flac_file_tags, VORBIS_TAG_KEYS.ALBUM_ARTISTS_NAMES))
    if album_artists_name_stringRaw is not None:
        return album_artists_name_stringRaw.strip()
    return None


def _get_genre_name_tag_from_flac_file_tags(flac_file_tags: FLAC):
    if VORBIS_TAG_KEYS.GENRE_NAME in flac_file_tags:
        return flac_file_tags[VORBIS_TAG_KEYS.GENRE_NAME][0]
    else:
        return ""


def _get_language_tag_from_flac_file_tags(flac_file: FLAC):
    return _get_first_value_if_exists_or_none(flac_file, VORBIS_TAG_KEYS.LANGUAGE)


def _get_specific_metadata_from_id3_file(
        id3_file_tags: MutagenFile, metadata_key: str, normalized_rating_max_value: int = None):
    if metadata_key == METADATA_DICT_KEYS.TITLE:
        return _get_title_tag_from_id3_file_tags(id3_file_tags)
    elif metadata_key == METADATA_DICT_KEYS.ARTIST_NAME:
        return _get_artist_name_tag_from_id3_file_tags(id3_file_tags)
    elif metadata_key == METADATA_DICT_KEYS.ALBUM_NAME:
        return _get_album_name_tag_from_id3_file_tags(id3_file_tags)
    elif metadata_key == METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES:
        return _get_album_artists_name_str_tag_from_id3_file_tags(id3_file_tags)
    elif metadata_key == METADATA_DICT_KEYS.GENRE_NAME:
        return _get_genre_name_tag_from_id3_file_tags(id3_file_tags)
    elif metadata_key == METADATA_DICT_KEYS.DURATION:
        return _get_duration_from_file_tags(id3_file_tags)
    elif metadata_key == METADATA_DICT_KEYS.RATING:
        return _get_eventually_normalized_rating_value_from_id3_file_tags(
            id3_file_tags, normalized_rating_max_value)
    elif metadata_key == METADATA_DICT_KEYS.LANGUAGE:
        return _get_language_tag_from_id3_file_tags(id3_file_tags)


def _get_specific_metadata_from_flac_file(
        flac_file_tags: FLAC, metadata_key: str, normalized_rating_max_value: Optional[int] = None):
    if metadata_key == METADATA_DICT_KEYS.TITLE:
        return _get_title_tag_from_flac_file_tags(flac_file_tags)
    elif metadata_key == METADATA_DICT_KEYS.ARTIST_NAME:
        return _get_artist_name_tagFrom_flac_file_tags(flac_file_tags)
    elif metadata_key == METADATA_DICT_KEYS.ALBUM_NAME:
        return _get_album_name_tagFrom_flac_file_tags(flac_file_tags)
    elif metadata_key == METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES:
        return _get_album_artists_nametring_tagFrom_flac_file_tags(flac_file_tags)
    elif metadata_key == METADATA_DICT_KEYS.GENRE_NAME:
        return _get_genre_name_tag_from_flac_file_tags(flac_file_tags)
    elif metadata_key == METADATA_DICT_KEYS.DURATION:
        return _get_duration_from_file_tags(flac_file_tags)
    elif metadata_key == METADATA_DICT_KEYS.RATING:
        return _get_eventually_normalized_rating_value_from_flac_file_tags(
            flac_file_tags, normalized_rating_max_value)
    elif metadata_key == METADATA_DICT_KEYS.LANGUAGE:
        return _get_language_tag_from_flac_file_tags(flac_file_tags)


def _get_id3_file_tags_updated_with_metadata_value(
        id3_file_tags: ID3,
        update_metadata_dict: dict,
        update_metadata_key: str,
        normalized_rating_max_value: int):
    if update_metadata_key == METADATA_DICT_KEYS.TITLE:
        id3_key = ID3_TEXT_FRAMES.TITLE
        text_frame_class = TIT2
    elif update_metadata_key == METADATA_DICT_KEYS.ARTIST_NAME:
        id3_key = ID3_TEXT_FRAMES.ARTIST_NAME
        text_frame_class = TPE1
    elif update_metadata_key == METADATA_DICT_KEYS.ALBUM_NAME:
        id3_key = ID3_TEXT_FRAMES.ALBUM_NAME
        text_frame_class = TALB
    elif update_metadata_key == METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES:
        id3_key = ID3_TEXT_FRAMES.ALBUM_ARTISTS_NAMES
        text_frame_class = TPE2
    elif update_metadata_key == METADATA_DICT_KEYS.GENRE_NAME:
        id3_key = ID3_TEXT_FRAMES.GENRE_NAME
        text_frame_class = TCON
    elif update_metadata_key == METADATA_DICT_KEYS.RATING:
        normalized_rating = update_metadata_dict[METADATA_DICT_KEYS.RATING]
        id3_file_tags.delall(ID3_TEXT_FRAMES.RATING)
        if normalized_rating is not None:
            id3_rating = _get_file_rating_from_normalized_value(
                normalized_rating=normalized_rating,
                normalized_rating_max_value=normalized_rating_max_value,
                rating_file_profile=RATING_FILE_PROFILE.BASE_255)
            id3_file_tags.add(POPM(email=ID3_RATING_APP_EMAIL, rating=id3_rating))
        return id3_file_tags
    elif update_metadata_key == METADATA_DICT_KEYS.LANGUAGE:
        id3_key = ID3_TEXT_FRAMES.LANGUAGE
        text_frame_class = TLAN
    else:
        raise KeyError(METADATA_DICT_UPDATE_KEY_NOT_HANDLED_MESSAGE)

    id3_file_tags.delall(id3_key)
    id3_file_tags.add(text_frame_class(encoding=3, text=update_metadata_dict[update_metadata_key]))

    return id3_file_tags


def _get_file_rating_from_normalized_value(
        normalized_rating: int, normalized_rating_max_value: int, rating_file_profile: str):
    star_rating_base_10 = (int)((normalized_rating * 10)/normalized_rating_max_value)
    if rating_file_profile == RATING_FILE_PROFILE.BASE_255:
        return BASE_255_RATING_STAR_VALUES[star_rating_base_10]
    else:
        return BASE_100_RATING_STAR_VALUES[star_rating_base_10]


def _get_flac_file_tags_updated_if_value_specified(
        flac_file_tags: FLAC,
        metadata_update_dict: dict,
        metadata_dictKey: str,
        normalized_rating_max_value: int):
    if metadata_dictKey in metadata_update_dict:
        if metadata_dictKey == METADATA_DICT_KEYS.TITLE:
            vorbis_tag_key = VORBIS_TAG_KEYS.TITLE
        elif metadata_dictKey == METADATA_DICT_KEYS.ARTIST_NAME:
            vorbis_tag_key = VORBIS_TAG_KEYS.ARTIST_NAME
        elif metadata_dictKey == METADATA_DICT_KEYS.ALBUM_NAME:
            vorbis_tag_key = VORBIS_TAG_KEYS.ALBUM_NAME
        elif metadata_dictKey == METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES:
            vorbis_tag_key = VORBIS_TAG_KEYS.ALBUM_ARTISTS_NAMES
        elif metadata_dictKey == METADATA_DICT_KEYS.GENRE_NAME:
            vorbis_tag_key = VORBIS_TAG_KEYS.GENRE_NAME
        elif metadata_dictKey == METADATA_DICT_KEYS.RATING:
            app_rating = metadata_update_dict[metadata_dictKey]
            vorbis_tag_key = VORBIS_TAG_KEYS.RATING
            if app_rating is not None:
                vorbis_rating = _get_file_rating_from_normalized_value(
                    normalized_rating=app_rating,
                    normalized_rating_max_value=normalized_rating_max_value,
                    rating_file_profile=RATING_FILE_PROFILE.BASE_100)
                metadata_update_dict[metadata_dictKey] = str(vorbis_rating)
        elif metadata_dictKey == METADATA_DICT_KEYS.LANGUAGE:
            vorbis_tag_key = VORBIS_TAG_KEYS.LANGUAGE
        else:
            raise KeyError(METADATA_DICT_UPDATE_KEY_NOT_HANDLED_MESSAGE)

        value = metadata_update_dict[metadata_dictKey]
        if value is not None:
            if vorbis_tag_key not in flac_file_tags:
                flac_file_tags[vorbis_tag_key] = [1]
            flac_file_tags[vorbis_tag_key] = metadata_update_dict[metadata_dictKey]
        elif vorbis_tag_key in flac_file_tags:
            del flac_file_tags[vorbis_tag_key]

    return flac_file_tags


def _get_first_value_if_exists_or_none(dict: dict, key: str):
    if key in dict:
        return dict[key][0]
    else:
        return None


def _get_first_value_int_if_exists_or_none(dict: dict, key: str):
    if key in dict:
        value_str = dict[key][0]
        if value_str != "":
            return int(value_str)
    return None
