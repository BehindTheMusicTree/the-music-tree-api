#!/usr/bin/env python
import os
from mutagen._file import File as MutagenFile
from mutagen.wave import WAVE
from mutagen.id3 import Frames
from mutagen.id3 import ID3
from mutagen.flac import FLAC
from mutagen.id3 import TIT2
from mutagen.id3 import TPE1
from mutagen.id3 import TALB
from mutagen.id3 import TPE2
from mutagen.id3 import TCON
from mutagen.id3 import POPM
from mutagen.id3 import TLAN
from mutagen.id3 import ID3NoHeaderError

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
    ARTIST_NAME = 'artistName'
    ALBUM_NAME = 'albumName'
    ALBUM_ARTISTS_NAMES = 'albumArtistsNameString'
    GENRE_NAME = 'genreName'
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


def Update(file, metadataUpdateDict: dict, normalizedRatingMaxValue: int):

    filename, fileExtension = os.path.splitext(file.name)
    fileExtensionLowered = fileExtension.lower()

    if fileExtensionLowered in [".wav", ".mp3"]:
        if fileExtensionLowered == ".mp3":
            try:
                fileTags = ID3(file)
            except ID3NoHeaderError:
                fileTags = ID3()
        if fileExtensionLowered == ".wav":
            mutagenWaveFile = WAVE()
            mutagenWaveFile.add_tags()
            fileTags = mutagenWaveFile.tags
            
            
        for metadataDictKey in list(metadataUpdateDict.keys()):
            if metadataDictKey == METADATA_DICT_KEYS.DURATION:
                raise ValueError(METADATA_DICT_UPDATE_DURATION_SHOULDNT_BE_SET_MESSAGE)
            else:
                fileTags = _getId3FileTagsUpdatedWithMetadataValue(
                        id3FileTags=fileTags, 
                        updateMetadataDict=metadataUpdateDict, 
                        updateMetadataKey=metadataDictKey,
                        normalizedRatingMaxValue=normalizedRatingMaxValue)

    elif fileExtensionLowered == ".flac":
        fileTags = FLAC(file)
        for metadataDictKey in list(metadataUpdateDict.keys()):
            if metadataDictKey == METADATA_DICT_KEYS.DURATION:
                raise ValueError(METADATA_DICT_UPDATE_DURATION_SHOULDNT_BE_SET_MESSAGE)
            else:
                fileTags = _getFlacFileTagsUpdatedIfValueSpecified(
                        flacFileTags=fileTags, 
                        metadataUpdateDict=metadataUpdateDict, 
                        metadataDictKey=metadataDictKey,
                        normalizedRatingMaxValue=normalizedRatingMaxValue)
    else:
        raise ValueError(FILE_EXTENSION_NOT_HANDLED_MESSAGE)
    fileTags.save(file.path)


def GetSpecificMetadataFromFile(file, metadataKey: str):
    filename, fileExtension = os.path.splitext(file.name)
    fileExtensionLowered = fileExtension.lower()
    if fileExtensionLowered in [".wav", ".mp3"]:
        fileTags = MutagenFile(file)
        return _getSpecificMetadataFromId3File(id3FileTags=fileTags, metadataKey=metadataKey)
    elif fileExtensionLowered == ".flac":
        flacFileTags = FLAC(fileobj=file)
        return _getSpecificMetadataFromFlacFile(flacFileTags=flacFileTags, metadataKey=metadataKey)    
    else:
        raise ValueError(FILE_EXTENSION_NOT_HANDLED_MESSAGE)
        

def GetMetadataDictFromFile(file, normalizedRatingMaxValue: int=None):
    filename, fileExtension = os.path.splitext(file.name)

    title = ""
    artistName = ""
    albumName = ""
    albumArtistsNameString = ""
    genreName = ""
    rating = None
    language = "" 
    
    fileExtensionLowered = fileExtension.lower()
    if fileExtensionLowered in [".wav", ".mp3"]:
        fileTags = MutagenFile(file)
        title = _getTitleTagFromId3FileTags(fileTags)
        artistName = _getArtistNameTagFromId3FileTags(fileTags)
        albumName = _getAlbumNameTagFromId3FileTags(fileTags)
        albumArtistsNameString = _getalbumArtistsNametringTagFromId3FileTags(fileTags)
        genreName = _getGenreNameTagFromId3FileTags(fileTags)
        rating = _getEventuallyNormalizedRatingValueFromId3FileTags(
                fileTags, normalizedRatingMaxValue) 
        language = _getLanguageTagFromId3FileTags(fileTags) 

    elif fileExtension.lower() == ".flac":
        fileTags = FLAC(fileobj=file)
        title = _getTitleTagFromFlacFileTags(fileTags)
        artistName = _getArtistNameTagFromFlacFileTags(fileTags)
        albumName = _getAlbumNameTagFromFlacFileTags(fileTags)
        albumArtistsNameString = _getAlbumArtistsNametringTagFromFlacFileTags(fileTags)
        genreName = _getGenreNameTagFromFlacFileTags(fileTags)
        rating = _getEventuallyNormalizedRatingValueFromFlacFileTags(fileTags, normalizedRatingMaxValue) 
        language = _getLanguageTagFromFlacFileTags(fileTags)
    else:
        raise ValueError(FILE_EXTENSION_NOT_HANDLED_MESSAGE)
    
    metadataDict = dict()
    metadataDict[METADATA_DICT_KEYS.TITLE] = title
    metadataDict[METADATA_DICT_KEYS.ARTIST_NAME] = artistName
    metadataDict[METADATA_DICT_KEYS.ALBUM_NAME] = albumName
    metadataDict[METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES] = albumArtistsNameString
    metadataDict[METADATA_DICT_KEYS.GENRE_NAME] = genreName
    metadataDict[METADATA_DICT_KEYS.DURATION] = _getDurationFromFileTags(fileTags=fileTags)
    metadataDict[METADATA_DICT_KEYS.RATING] = rating
    metadataDict[METADATA_DICT_KEYS.LANGUAGE] = language
    return metadataDict


def _getDurationFromFileTags(fileTags):
    return fileTags.info.length


def _getTitleTagFromId3FileTags(id3FileTags: MutagenFile):
    return _getFirstValueIfExistsOrNone(id3FileTags, ID3_TEXT_FRAMES.TITLE)


def _getArtistNameTagFromId3FileTags(id3FileTags: MutagenFile):
    return _getFirstValueIfExistsOrNone(id3FileTags, ID3_TEXT_FRAMES.ARTIST_NAME)


def _getAlbumNameTagFromId3FileTags(id3FileTags: MutagenFile):
    return _getFirstValueIfExistsOrNone(id3FileTags, ID3_TEXT_FRAMES.ALBUM_NAME)


def _getalbumArtistsNametringTagFromId3FileTags(id3FileTags: MutagenFile):
    albumArtistsNameStringRaw = (
            _getFirstValueIfExistsOrNone(id3FileTags, ID3_TEXT_FRAMES.ALBUM_ARTISTS_NAMES))
    return albumArtistsNameStringRaw.strip()


def _getGenreNameTagFromId3FileTags(id3FileTags: MutagenFile):
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
   

def _getEventuallyNormalizedRatingValueFromId3FileTags(
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
    
    
def _getLanguageTagFromId3FileTags(id3FileTags: MutagenFile):
    return _getFirstValueIfExistsOrNone(id3FileTags, ID3_TEXT_FRAMES.LANGUAGE)


def _getTitleTagFromFlacFileTags(flacFileTags: FLAC):
    return _getFirstValueIfExistsOrNone(flacFileTags, VORBIS_TAG_KEYS.TITLE)


def _getArtistNameTagFromFlacFileTags(flacFileTags: FLAC):
    return _getFirstValueIfExistsOrNone(flacFileTags, VORBIS_TAG_KEYS.ARTIST_NAME)


def _getAlbumNameTagFromFlacFileTags(flacFileTags: FLAC):
    return _getFirstValueIfExistsOrNone(flacFileTags, VORBIS_TAG_KEYS.ALBUM_NAME)


def _getAlbumArtistsNametringTagFromFlacFileTags(flacFileTags: FLAC):
    albumArtistsNameStringRaw = (
            _getFirstValueIfExistsOrNone(
                    flacFileTags, VORBIS_TAG_KEYS.ALBUM_ARTISTS_NAMES))
    return albumArtistsNameStringRaw.strip()


def _getGenreNameTagFromFlacFileTags(flacFileTags: FLAC):
    if VORBIS_TAG_KEYS.GENRE_NAME in flacFileTags:
        return flacFileTags[VORBIS_TAG_KEYS.GENRE_NAME][0]
    else:
        return ""
    

def _getLanguageTagFromFlacFileTags(flacFile: FLAC):
    return _getFirstValueIfExistsOrNone(flacFile, VORBIS_TAG_KEYS.LANGUAGE)


def _getSpecificMetadataFromId3File(
            id3FileTags: MutagenFile, metadataKey: str, normalizedRatingMaxValue: int=None):
    if metadataKey == METADATA_DICT_KEYS.TITLE:
        return _getTitleTagFromId3FileTags(id3FileTags)
    elif metadataKey == METADATA_DICT_KEYS.ARTIST_NAME:
        return _getArtistNameTagFromId3FileTags(id3FileTags)
    elif metadataKey == METADATA_DICT_KEYS.ALBUM_NAME:
        return _getAlbumNameTagFromId3FileTags(id3FileTags)
    elif metadataKey == METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES:
        return _getalbumArtistsNametringTagFromId3FileTags(id3FileTags)
    elif metadataKey == METADATA_DICT_KEYS.GENRE_NAME:
        return _getGenreNameTagFromId3FileTags(id3FileTags)
    elif metadataKey == METADATA_DICT_KEYS.DURATION:
        return _getDurationFromFileTags(id3FileTags)
    elif metadataKey == METADATA_DICT_KEYS.RATING:
        return _getEventuallyNormalizedRatingValueFromId3FileTags(
                id3FileTags, normalizedRatingMaxValue)
    elif metadataKey == METADATA_DICT_KEYS.LANGUAGE:
        return _getLanguageTagFromId3FileTags(id3FileTags)


def _getSpecificMetadataFromFlacFile(
        flacFileTags: FLAC, metadataKey: str, normalizedRatingMaxValue: int = None):
    if metadataKey == METADATA_DICT_KEYS.TITLE:
        return _getTitleTagFromFlacFileTags(flacFileTags)
    elif metadataKey == METADATA_DICT_KEYS.ARTIST_NAME:
        return _getArtistNameTagFromFlacFileTags(flacFileTags)
    elif metadataKey == METADATA_DICT_KEYS.ALBUM_NAME:
        return _getAlbumNameTagFromFlacFileTags(flacFileTags)
    elif metadataKey == METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES:
        return _getAlbumArtistsNametringTagFromFlacFileTags(flacFileTags)
    elif metadataKey == METADATA_DICT_KEYS.GENRE_NAME:
        return _getGenreNameTagFromFlacFileTags(flacFileTags)
    elif metadataKey == METADATA_DICT_KEYS.DURATION:
        return _getDurationFromFileTags(flacFileTags)
    elif metadataKey == METADATA_DICT_KEYS.RATING:
        return _getEventuallyNormalizedRatingValueFromFlacFileTags(
                flacFileTags, normalizedRatingMaxValue)
    elif metadataKey == METADATA_DICT_KEYS.LANGUAGE:
        return _getLanguageTagFromFlacFileTags(flacFileTags)


def _getId3FileTagsUpdatedWithMetadataValue(
        id3FileTags: ID3, 
        updateMetadataDict: dict, 
        updateMetadataKey: str, 
        normalizedRatingMaxValue: int):
    if updateMetadataKey == METADATA_DICT_KEYS.TITLE:
        id3Key = ID3_TEXT_FRAMES.TITLE
        textFrameClass = TIT2
    elif updateMetadataKey == METADATA_DICT_KEYS.ARTIST_NAME:
        id3Key = ID3_TEXT_FRAMES.ARTIST_NAME
        textFrameClass = TPE1
    elif updateMetadataKey == METADATA_DICT_KEYS.ALBUM_NAME:
        id3Key = ID3_TEXT_FRAMES.ALBUM_NAME
        textFrameClass = TALB
    elif updateMetadataKey == METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES:
        id3Key = ID3_TEXT_FRAMES.ALBUM_ARTISTS_NAMES
        textFrameClass = TPE2
    elif updateMetadataKey == METADATA_DICT_KEYS.GENRE_NAME:
        id3Key = ID3_TEXT_FRAMES.GENRE_NAME
        textFrameClass = TCON
    elif updateMetadataKey == METADATA_DICT_KEYS.RATING:
        normalizedRating = updateMetadataDict[METADATA_DICT_KEYS.RATING]
        id3FileTags.delall(ID3_TEXT_FRAMES.RATING)
        if normalizedRating is not None:
            id3Rating = _getFileRatingFromNormalizedValue(
                    normalizedRating=normalizedRating, 
                    normalizedRatingMaxValue=normalizedRatingMaxValue, 
                    ratingFileProfile=RATING_FILE_PROFILE.BASE_255)
            id3FileTags.add(POPM(email=ID3_RATING_APP_EMAIL, rating=id3Rating))
        return id3FileTags
    elif updateMetadataKey == METADATA_DICT_KEYS.LANGUAGE:
        id3Key = ID3_TEXT_FRAMES.LANGUAGE
        textFrameClass = TLAN
    else:
        raise KeyError(METADATA_DICT_UPDATE_KEY_NOT_HANDLED_MESSAGE)
    
    id3FileTags.delall(id3Key)
    id3FileTags.add(textFrameClass(encoding=3, text=updateMetadataDict[updateMetadataKey]))

    return id3FileTags


def _getFileRatingFromNormalizedValue(
        normalizedRating: int, normalizedRatingMaxValue: int, ratingFileProfile: str):
    starRatingBase10 = (int)((normalizedRating * 10)/normalizedRatingMaxValue)
    if ratingFileProfile == RATING_FILE_PROFILE.BASE_255:
        return BASE_255_RATING_STAR_VALUES[starRatingBase10]
    else:
        return BASE_100_RATING_STAR_VALUES[starRatingBase10]
    

def _getFlacFileTagsUpdatedIfValueSpecified(
        flacFileTags: FLAC, 
        metadataUpdateDict: dict, 
        metadataDictKey: str, 
        normalizedRatingMaxValue: int):
    if metadataDictKey in metadataUpdateDict:
        if metadataDictKey == METADATA_DICT_KEYS.TITLE:
            vorbisTagKey = VORBIS_TAG_KEYS.TITLE
        elif metadataDictKey == METADATA_DICT_KEYS.ARTIST_NAME:
            vorbisTagKey = VORBIS_TAG_KEYS.ARTIST_NAME
        elif metadataDictKey == METADATA_DICT_KEYS.ALBUM_NAME:
            vorbisTagKey = VORBIS_TAG_KEYS.ALBUM_NAME
        elif metadataDictKey == METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES:
            vorbisTagKey = VORBIS_TAG_KEYS.ALBUM_ARTISTS_NAMES
        elif metadataDictKey == METADATA_DICT_KEYS.GENRE_NAME:
            vorbisTagKey = VORBIS_TAG_KEYS.GENRE_NAME
        elif metadataDictKey == METADATA_DICT_KEYS.RATING:
            appRating = metadataUpdateDict[metadataDictKey]
            vorbisTagKey = VORBIS_TAG_KEYS.RATING
            if appRating is not None:
                vorbisRating = _getFileRatingFromNormalizedValue(
                        normalizedRating=appRating, 
                        normalizedRatingMaxValue=normalizedRatingMaxValue, 
                        ratingFileProfile=RATING_FILE_PROFILE.BASE_100)
                metadataUpdateDict[metadataDictKey] = str(vorbisRating)
        elif metadataDictKey == METADATA_DICT_KEYS.LANGUAGE:
            vorbisTagKey = VORBIS_TAG_KEYS.LANGUAGE
        else:
            raise KeyError(METADATA_DICT_UPDATE_KEY_NOT_HANDLED_MESSAGE)
        
        value = metadataUpdateDict[metadataDictKey]
        if value is not None:
            if vorbisTagKey not in flacFileTags:
                flacFileTags[vorbisTagKey] = [1]
            flacFileTags[vorbisTagKey] = metadataUpdateDict[metadataDictKey]
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
