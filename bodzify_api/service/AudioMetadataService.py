#!/usr/bin/env python
import io
import os
from typing import Optional
from mutagen._file import File as MutagenFile
from mutagen.wave import WAVE
from mutagen.id3 import Frames
from mutagen.id3 import ID3
from mutagen.flac import FLAC
from mutagen.id3._frames import TIT2
from mutagen.id3._frames import TPE1
from mutagen.id3._frames import TALB
from mutagen.id3._frames import TPE2
from mutagen.id3._frames import TCON
from mutagen.id3._frames import POPM
from mutagen.id3._frames import TLAN
from mutagen.id3._util import ID3NoHeaderError
from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile


TAG_ARTISTS_SEPARATION_CHAR = ","

# MP3 and Wave (.wav) files use ID3 tags
class ID3_TEXT_FRAMES:
    TITLE = 'TIT2'
    ARTIST_NAME = 'TPE1'
    ALBUM_NAME = 'TALB'
    ALBUM_ARTISTS_NAMES = 'TPE2'
    GENRE_NAME = 'TCON'
    RATING = 'POPM'
    LANGUAGE = 'TLAN'
    
ID3_RATING_APP_EMAIL = 'bodzify'

# FLAC files use Vorbis tags
class VORBIS_TAG_KEYS:
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
    
BASE_255_RATING_STAR_VALUES = [0, 13, 1, 54, 64, 118, 128, 186, 196, 242, 255]
BASE_255_PROPORTIONAL_RATING_STAR_VALUES = [
        None, None, 51, None, 102, None, 153, None, 204, None, 255]
BASE_100_RATING_STAR_VALUES = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

TRAKTOR_RATING_TAG_MAIL = 'traktor@native-instruments.de'

FILE_EXTENSION_NOT_HANDLED_MESSAGE = "The file's format is not handled by the service."
METADATA_DICT_UPDATE_DURATION_SHOULDNT_BE_SET_MESSAGE = """The duration key has a value in the 
metadata dict. The duration cannot be updated. It is therefore ignored."""
METADATA_DICT_UPDATE_KEY_NOT_HANDLED_MESSAGE = """The specified audio metadata key is not 
handled by the service."""


def update(file, metadata_update_dict: dict, normalized_rating_max_value: int):

    filename, file_extension = os.path.splitext(file.name)
    file_extension_lowered = file_extension.lower()

    if file_extension_lowered in [".wav", ".mp3"]:
        if file_extension_lowered == ".mp3":
            try:
                file_tags = ID3(file)
            except ID3NoHeaderError:
                file_tags = ID3()
        if file_extension_lowered == ".wav":
            mutagen_wave_file = WAVE()
            mutagen_wave_file.add_tags()
            file_tags = mutagen_wave_file.tags
            
            
        for metadata_dict_key in list(metadata_update_dict.keys()):
            if metadata_dict_key == METADATA_DICT_KEYS.DURATION:
                raise ValueError(METADATA_DICT_UPDATE_DURATION_SHOULDNT_BE_SET_MESSAGE)
            else:
                file_tags = _get_id3_file_tags_updated_with_metadata_value(
                        id3_file_tags=file_tags, 
                        update_metadata_dict=metadata_update_dict, 
                        update_metadata_key=metadata_dict_key,
                        normalizedRatingMaxValue=normalized_rating_max_value)

    elif file_extension_lowered == ".flac":
        file_tags = _create_flac_object_dealing_with_eventual_temporary_file(file)
        for metadata_dict_key in list(metadata_update_dict.keys()):
            if metadata_dict_key == METADATA_DICT_KEYS.DURATION:
                raise ValueError(METADATA_DICT_UPDATE_DURATION_SHOULDNT_BE_SET_MESSAGE)
            else:
                file_tags = _getFlacFileTagsUpdatedIfValueSpecified(
                        flacFileTags=file_tags, 
                        metadata_update_dict=metadata_update_dict, 
                        metadata_dictKey=metadata_dict_key,
                        normalizedRatingMaxValue=normalized_rating_max_value)
    else:
        raise ValueError(FILE_EXTENSION_NOT_HANDLED_MESSAGE)
    file_tags.save(file.path)


def get_specific_metadata_from_file(file, metadata_key: str):
    filename, fileExtension = os.path.splitext(file.name)
    fileExtensionLowered = fileExtension.lower()
    if fileExtensionLowered in [".wav", ".mp3"]:
        fileTags = MutagenFile(file)
        return _getSpecificMetadataFromId3File(id3FileTags=fileTags, metadataKey=metadata_key)
    elif fileExtensionLowered == ".flac":
        flacFileTags = _create_flac_object_dealing_with_eventual_temporary_file(file)
        return _getSpecificMetadataFromFlacFile(flacFileTags=flacFileTags, metadataKey=metadata_key)    
    else:
        raise ValueError(FILE_EXTENSION_NOT_HANDLED_MESSAGE)


def _create_flac_object_dealing_with_eventual_temporary_file(file):
    if isinstance(file, TemporaryUploadedFile):
        with open(file.temporary_file_path(), 'rb') as f:
            return FLAC(fileobj=io.BytesIO(f.read()))
    elif isinstance(file, InMemoryUploadedFile):
        file.seek(0)
        return FLAC(io.BytesIO(file.read()))
    return FLAC(fileobj=file)
        

def get_metadata_dict_from_file(file, normalized_rating_max_value: Optional[int] = None):
    filename, fileExtension = os.path.splitext(file.name)

    title = ""
    artist_name = ""
    album_name = ""
    album_artists_name_string = ""
    genre_name = ""
    rating = None
    language = "" 
    
    fileExtensionLowered = fileExtension.lower()
    if fileExtensionLowered in [".wav", ".mp3"]:
        fileTags = MutagenFile(file)
        title = _getTitleTagFromId3FileTags(fileTags)
        artist_name = _getartist_name_tagFromId3FileTags(fileTags)
        album_name = _getalbum_name_tagFromId3FileTags(fileTags)
        album_artists_name_string = _getalbum_artistsNametringTagFromId3FileTags(fileTags)
        genre_name = _getgenre_name_tagFromId3FileTags(fileTags)
        rating = _get_eventually_normalized_rating_value_from_id3_file_tags(
                fileTags, normalized_rating_max_value) 
        language = _getlanguage_tagFromId3FileTags(fileTags) 

    elif fileExtension.lower() == ".flac":
        fileTags = _create_flac_object_dealing_with_eventual_temporary_file(file)
        title = _getTitleTagFromFlacFileTags(fileTags)
        artist_name = _getartist_name_tagFromFlacFileTags(fileTags)
        album_name = _getalbum_name_tagFromFlacFileTags(fileTags)
        album_artists_name_string = _getalbum_artistsNametringTagFromFlacFileTags(fileTags)
        genre_name = _getgenre_name_tagFromFlacFileTags(fileTags)
        rating = _getEventuallyNormalizedRatingValueFromFlacFileTags(fileTags, normalized_rating_max_value) 
        language = _getlanguage_tagFromFlacFileTags(fileTags)
    else:
        raise ValueError(FILE_EXTENSION_NOT_HANDLED_MESSAGE)
    
    metadata_dict = dict()
    metadata_dict[METADATA_DICT_KEYS.TITLE] = title
    metadata_dict[METADATA_DICT_KEYS.ARTIST_NAME] = artist_name
    metadata_dict[METADATA_DICT_KEYS.ALBUM_NAME] = album_name
    metadata_dict[METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES] = album_artists_name_string
    metadata_dict[METADATA_DICT_KEYS.GENRE_NAME] = genre_name
    metadata_dict[METADATA_DICT_KEYS.DURATION] = _get_duration_from_file_tags(fileTags=fileTags)
    metadata_dict[METADATA_DICT_KEYS.RATING] = rating
    metadata_dict[METADATA_DICT_KEYS.LANGUAGE] = language
    return metadata_dict


def _get_duration_from_file_tags(fileTags):
    return fileTags.info.length


def _getTitleTagFromId3FileTags(id3FileTags: MutagenFile):
    return _getFirstValueIfExistsOrNone(id3FileTags, ID3_TEXT_FRAMES.TITLE)


def _getartist_name_tagFromId3FileTags(id3FileTags: MutagenFile):
    return _getFirstValueIfExistsOrNone(id3FileTags, ID3_TEXT_FRAMES.ARTIST_NAME)


def _getalbum_name_tagFromId3FileTags(id3FileTags: MutagenFile):
    return _getFirstValueIfExistsOrNone(id3FileTags, ID3_TEXT_FRAMES.ALBUM_NAME)


def _getalbum_artistsNametringTagFromId3FileTags(id3FileTags: MutagenFile):
    album_artistsname_stringRaw = (
            _getFirstValueIfExistsOrNone(id3FileTags, ID3_TEXT_FRAMES.ALBUM_ARTISTS_NAMES))
    if album_artistsname_stringRaw is not None:
        return album_artistsname_stringRaw.strip()
    return None


def _getgenre_name_tagFromId3FileTags(id3FileTags: MutagenFile):
    if ID3_TEXT_FRAMES.GENRE_NAME in id3FileTags:
        return id3FileTags[ID3_TEXT_FRAMES.GENRE_NAME][0]
    else:
        return ""


def _getEventuallyNormalizedRatingFromFileValue(
    fileRatingValue: int, normalizedRatingMaxValue: int, isRatingFromTraktor: bool=False):
    if fileRatingValue is not None:
        if normalizedRatingMaxValue is not None:
            if fileRatingValue == 0 and isRatingFromTraktor:
                return None
            for starRatingBase10 in range(11):
                if fileRatingValue in [
                    BASE_255_RATING_STAR_VALUES[starRatingBase10], 
                    BASE_255_PROPORTIONAL_RATING_STAR_VALUES[starRatingBase10], 
                    BASE_100_RATING_STAR_VALUES[starRatingBase10]]:
                    return int(starRatingBase10 * normalizedRatingMaxValue / 10)
            raise ValueError("Rating value not handled: " + str(fileRatingValue))
        else:
            return fileRatingValue
    else:
        return None
   

def _get_eventually_normalized_rating_value_from_id3_file_tags(
        id3FileTags: MutagenFile, normalizedRatingMaxValue: int):
    fileRatingValue = None
    for key in id3FileTags:
        if ID3_TEXT_FRAMES.RATING in key:
            fileRatingTag = id3FileTags[key]
            fileRatingEmail = fileRatingTag.email
            fileRatingValue = fileRatingTag.rating            
    if fileRatingValue is None:
        return None
    else:
        return _getEventuallyNormalizedRatingFromFileValue(
                fileRatingValue=fileRatingValue, 
                isRatingFromTraktor=(fileRatingEmail == TRAKTOR_RATING_TAG_MAIL), 
                normalizedRatingMaxValue=normalizedRatingMaxValue)


def _getEventuallyNormalizedRatingValueFromFlacFileTags(
        flacFileTags: FLAC, normalizedRatingMaxValue: int=None):
    fileRating = _getFirstValueIntIfExistsOrNone(flacFileTags, VORBIS_TAG_KEYS.RATING)
    isRatingFromTraktor = False
    if fileRating is None:
        fileRating = _getFirstValueIntIfExistsOrNone(flacFileTags, VORBIS_TAG_KEYS.RATING_TRAKTOR)
        if fileRating is not None:
            isRatingFromTraktor = True

    if fileRating is None or fileRating == "":
        return None
    else:
        return _getEventuallyNormalizedRatingFromFileValue(
                fileRatingValue=fileRating, 
                isRatingFromTraktor=isRatingFromTraktor,
                normalizedRatingMaxValue=normalizedRatingMaxValue)
    
    
def _getlanguage_tagFromId3FileTags(id3FileTags: MutagenFile):
    return _getFirstValueIfExistsOrNone(id3FileTags, ID3_TEXT_FRAMES.LANGUAGE)


def _getTitleTagFromFlacFileTags(flacFileTags: FLAC):
    return _getFirstValueIfExistsOrNone(flacFileTags, VORBIS_TAG_KEYS.TITLE)


def _getartist_name_tagFromFlacFileTags(flacFileTags: FLAC):
    return _getFirstValueIfExistsOrNone(flacFileTags, VORBIS_TAG_KEYS.ARTIST_NAME)


def _getalbum_name_tagFromFlacFileTags(flacFileTags: FLAC):
    return _getFirstValueIfExistsOrNone(flacFileTags, VORBIS_TAG_KEYS.ALBUM_NAME)


def _getalbum_artistsNametringTagFromFlacFileTags(flacFileTags: FLAC):
    album_artistsname_stringRaw = (
            _getFirstValueIfExistsOrNone(
                    flacFileTags, VORBIS_TAG_KEYS.ALBUM_ARTISTS_NAMES))
    if album_artistsname_stringRaw is not None:
        return album_artistsname_stringRaw.strip()
    return None


def _getgenre_name_tagFromFlacFileTags(flacFileTags: FLAC):
    if VORBIS_TAG_KEYS.GENRE_NAME in flacFileTags:
        return flacFileTags[VORBIS_TAG_KEYS.GENRE_NAME][0]
    else:
        return ""
    

def _getlanguage_tagFromFlacFileTags(flacFile: FLAC):
    return _getFirstValueIfExistsOrNone(flacFile, VORBIS_TAG_KEYS.LANGUAGE)


def _getSpecificMetadataFromId3File(
            id3FileTags: MutagenFile, metadataKey: str, normalizedRatingMaxValue: int=None):
    if metadataKey == METADATA_DICT_KEYS.TITLE:
        return _getTitleTagFromId3FileTags(id3FileTags)
    elif metadataKey == METADATA_DICT_KEYS.ARTIST_NAME:
        return _getartist_name_tagFromId3FileTags(id3FileTags)
    elif metadataKey == METADATA_DICT_KEYS.ALBUM_NAME:
        return _getalbum_name_tagFromId3FileTags(id3FileTags)
    elif metadataKey == METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES:
        return _getalbum_artistsNametringTagFromId3FileTags(id3FileTags)
    elif metadataKey == METADATA_DICT_KEYS.GENRE_NAME:
        return _getgenre_name_tagFromId3FileTags(id3FileTags)
    elif metadataKey == METADATA_DICT_KEYS.DURATION:
        return _get_duration_from_file_tags(id3FileTags)
    elif metadataKey == METADATA_DICT_KEYS.RATING:
        return _get_eventually_normalized_rating_value_from_id3_file_tags(
                id3FileTags, normalizedRatingMaxValue)
    elif metadataKey == METADATA_DICT_KEYS.LANGUAGE:
        return _getlanguage_tagFromId3FileTags(id3FileTags)


def _getSpecificMetadataFromFlacFile(
        flacFileTags: FLAC, metadataKey: str, normalizedRatingMaxValue: int = None):
    if metadataKey == METADATA_DICT_KEYS.TITLE:
        return _getTitleTagFromFlacFileTags(flacFileTags)
    elif metadataKey == METADATA_DICT_KEYS.ARTIST_NAME:
        return _getartist_name_tagFromFlacFileTags(flacFileTags)
    elif metadataKey == METADATA_DICT_KEYS.ALBUM_NAME:
        return _getalbum_name_tagFromFlacFileTags(flacFileTags)
    elif metadataKey == METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES:
        return _getalbum_artistsNametringTagFromFlacFileTags(flacFileTags)
    elif metadataKey == METADATA_DICT_KEYS.GENRE_NAME:
        return _getgenre_name_tagFromFlacFileTags(flacFileTags)
    elif metadataKey == METADATA_DICT_KEYS.DURATION:
        return _get_duration_from_file_tags(flacFileTags)
    elif metadataKey == METADATA_DICT_KEYS.RATING:
        return _getEventuallyNormalizedRatingValueFromFlacFileTags(
                flacFileTags, normalizedRatingMaxValue)
    elif metadataKey == METADATA_DICT_KEYS.LANGUAGE:
        return _getlanguage_tagFromFlacFileTags(flacFileTags)


def _get_id3_file_tags_updated_with_metadata_value(
        id3_file_tags: ID3, 
        update_metadata_dict: dict, 
        update_metadata_key: str, 
        normalizedRatingMaxValue: int):
    if update_metadata_key == METADATA_DICT_KEYS.TITLE:
        id3Key = ID3_TEXT_FRAMES.TITLE
        textFrameClass = TIT2
    elif update_metadata_key == METADATA_DICT_KEYS.ARTIST_NAME:
        id3Key = ID3_TEXT_FRAMES.ARTIST_NAME
        textFrameClass = TPE1
    elif update_metadata_key == METADATA_DICT_KEYS.ALBUM_NAME:
        id3Key = ID3_TEXT_FRAMES.ALBUM_NAME
        textFrameClass = TALB
    elif update_metadata_key == METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES:
        id3Key = ID3_TEXT_FRAMES.ALBUM_ARTISTS_NAMES
        textFrameClass = TPE2
    elif update_metadata_key == METADATA_DICT_KEYS.GENRE_NAME:
        id3Key = ID3_TEXT_FRAMES.GENRE_NAME
        textFrameClass = TCON
    elif update_metadata_key == METADATA_DICT_KEYS.RATING:
        normalizedRating = update_metadata_dict[METADATA_DICT_KEYS.RATING]
        id3_file_tags.delall(ID3_TEXT_FRAMES.RATING)
        if normalizedRating is not None:
            id3Rating = _getFileRatingFromNormalizedValue(
                    normalizedRating=normalizedRating, 
                    normalizedRatingMaxValue=normalizedRatingMaxValue, 
                    ratingFileProfile=RATING_FILE_PROFILE.BASE_255)
            id3_file_tags.add(POPM(email=ID3_RATING_APP_EMAIL, rating=id3Rating))
        return id3_file_tags
    elif update_metadata_key == METADATA_DICT_KEYS.LANGUAGE:
        id3Key = ID3_TEXT_FRAMES.LANGUAGE
        textFrameClass = TLAN
    else:
        raise KeyError(METADATA_DICT_UPDATE_KEY_NOT_HANDLED_MESSAGE)
    
    id3_file_tags.delall(id3Key)
    id3_file_tags.add(textFrameClass(encoding=3, text=update_metadata_dict[update_metadata_key]))

    return id3_file_tags


def _getFileRatingFromNormalizedValue(
        normalizedRating: int, normalizedRatingMaxValue: int, ratingFileProfile: str):
    starRatingBase10 = (int)((normalizedRating * 10)/normalizedRatingMaxValue)
    if ratingFileProfile == RATING_FILE_PROFILE.BASE_255:
        return BASE_255_RATING_STAR_VALUES[starRatingBase10]
    else:
        return BASE_100_RATING_STAR_VALUES[starRatingBase10]
    

def _getFlacFileTagsUpdatedIfValueSpecified(
        flacFileTags: FLAC, 
        metadata_update_dict: dict, 
        metadata_dictKey: str, 
        normalizedRatingMaxValue: int):
    if metadata_dictKey in metadata_update_dict:
        if metadata_dictKey == METADATA_DICT_KEYS.TITLE:
            vorbisTagKey = VORBIS_TAG_KEYS.TITLE
        elif metadata_dictKey == METADATA_DICT_KEYS.ARTIST_NAME:
            vorbisTagKey = VORBIS_TAG_KEYS.ARTIST_NAME
        elif metadata_dictKey == METADATA_DICT_KEYS.ALBUM_NAME:
            vorbisTagKey = VORBIS_TAG_KEYS.ALBUM_NAME
        elif metadata_dictKey == METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES:
            vorbisTagKey = VORBIS_TAG_KEYS.ALBUM_ARTISTS_NAMES
        elif metadata_dictKey == METADATA_DICT_KEYS.GENRE_NAME:
            vorbisTagKey = VORBIS_TAG_KEYS.GENRE_NAME
        elif metadata_dictKey == METADATA_DICT_KEYS.RATING:
            appRating = metadata_update_dict[metadata_dictKey]
            vorbisTagKey = VORBIS_TAG_KEYS.RATING
            if appRating is not None:
                vorbisRating = _getFileRatingFromNormalizedValue(
                        normalizedRating=appRating, 
                        normalizedRatingMaxValue=normalizedRatingMaxValue, 
                        ratingFileProfile=RATING_FILE_PROFILE.BASE_100)
                metadata_update_dict[metadata_dictKey] = str(vorbisRating)
        elif metadata_dictKey == METADATA_DICT_KEYS.LANGUAGE:
            vorbisTagKey = VORBIS_TAG_KEYS.LANGUAGE
        else:
            raise KeyError(METADATA_DICT_UPDATE_KEY_NOT_HANDLED_MESSAGE)
        
        value = metadata_update_dict[metadata_dictKey]
        if value is not None:
            if vorbisTagKey not in flacFileTags:
                flacFileTags[vorbisTagKey] = [1]
            flacFileTags[vorbisTagKey] = metadata_update_dict[metadata_dictKey]
        elif vorbisTagKey in flacFileTags:
            del flacFileTags[vorbisTagKey]

    return flacFileTags


def _getFirstValueIfExistsOrNone(dict: dict, key: str):
    if key in dict:
        return dict[key][0]
    else:
        return None


def _getFirstValueIntIfExistsOrNone(dict: dict, key: str):
    if key in dict:
        valueString = dict[key][0]
        if valueString != "":
            return int(valueString)
    return None
