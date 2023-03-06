#!/usr/bin/env python
import os
from mutagen._file import File as MutagenFile
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
ID3_TITLE_TEXT_FRAME = 'TIT2'
ID3_ARTIST_NAME_TEXT_FRAME = 'TPE1'
ID3_ALBUM_NAME_TEXT_FRAME = 'TALB'
ID3_ALBUM_ARTISTS_NAMES_TEXT_FRAME = 'TPE2'
ID3_GENRE_NAME_TEXT_FRAME = 'TCON'
ID3_RATING_TEXT_FRAME = 'POPM'
ID3_RATING_APP_EMAIL = 'POPM:bodzify'
ID3_RATING_MAX_VALUE = 255
ID3_LANGUAGE_TEXT_FRAME = 'TLAN'

# FLAC files use Vorbis tags
VORBIS_TITLE_TAG_KEY = 'title'
VORBIS_ARTIST_NAME_TAG_KEY = 'artist'
VORBIS_ALBUM_NAME_TAG_KEY = 'album'
VORBIS_ALBUM_ARTISTS_NAMES_TAG_KEY = 'albumartist'
VORBIS_GENRE_NAME_TAG_KEY = 'genre'
VORBIS_RATING_TAG_KEY = 'rating'
VORBIS_RATING_MAX_VALUE = 100
VORBIS_LANGUAGE_TAG_KEY = 'language'

METADATA_DICT_TITLE_KEY = "title"
METADATA_DICT_ARTIST_NAME_KEY = "artistName"
METADATA_DICT_ALBUM_NAME_KEY = "albumName"
METADATA_DICT_ALBUM_ARTISTS_NAME_STRING_KEY = "albumArtistsNameString"
METADATA_DICT_GENRE_NAME_KEY = "genreName"
METADATA_DICT_DURATION_KEY = "duration"
METADATA_DICT_RATING_KEY = "rating"
METADATA_DICT_LANGUAGE_KEY = "language"

FILE_EXTENSION_NOT_HANDLED_MESSAGE = "The file's format is not handled by the service."
METADATA_DICT_UPDATE_DURATION_SHOULDNT_BE_SET_MESSAGE = """The duration key has a value in the 
metadata dict. The duration cannot be updated. It is therefore ignored."""
METADATA_DICT_UPDATE_KEY_NOT_HANDLED_MESSAGE = """The specified audio metadata key is not 
handled by the service."""


def Update(file, metadataUpdateDict: dict, appRatingMaxValue: int):

    filename, fileExtension = os.path.splitext(file.name)
    fileExtensionLowered = fileExtension.lower()

    if fileExtensionLowered in [".wav", ".mp3"]:
        try:
            fileTags = ID3(file.path)
        except ID3NoHeaderError:
            fileTags = ID3()
        for metadataDictKey in list(metadataUpdateDict.keys()):
            if metadataDictKey == METADATA_DICT_DURATION_KEY:
                raise ValueError(METADATA_DICT_UPDATE_DURATION_SHOULDNT_BE_SET_MESSAGE)
            else:
                fileTags = _getId3FileTagsUpdatedIfTagValueSpecified(
                        id3FileTags=fileTags, 
                        updateMetadataDict=metadataUpdateDict, 
                        updateMetadataKey=metadataDictKey,
                        appMaxRating=appRatingMaxValue)

    elif fileExtensionLowered == ".flac":
        fileTags = FLAC(file.path)
        for metadataDictKey in list(metadataUpdateDict.keys()):
            if metadataDictKey == METADATA_DICT_DURATION_KEY:
                raise ValueError(METADATA_DICT_UPDATE_DURATION_SHOULDNT_BE_SET_MESSAGE)
            else:
                fileTags = _getFlacFileTagsUpdatedIfValueSpecified(
                        flacFile=fileTags, 
                        metadataUpdateDict=metadataUpdateDict, 
                        metadataDictKey=metadataDictKey)
    else:
        raise ValueError(FILE_EXTENSION_NOT_HANDLED_MESSAGE)

    fileTags.save(file.path)


def GetSpecificMetadataFromFile(file, metadataKey: str):
    filename, fileExtension = os.path.splitext(file.name)
    fileExtensionLowered = fileExtension.lower()
    if fileExtensionLowered in [".wav", ".mp3"]:
        mutagenFile = MutagenFile(file)
        return _getSpecificMetadataFromId3File(id3FileTags=mutagenFile, metadataKey=metadataKey)
    elif fileExtensionLowered == ".flac":
        flacFileTags = FLAC(fileobj=file)
        return _getSpecificMetadataFromFlacFile(flacFileTags=flacFileTags, metadataKey=metadataKey)    
    else:
        raise ValueError(FILE_EXTENSION_NOT_HANDLED_MESSAGE)
        

def GetMetadataDictFromFile(file, appRatingMaxValue: int):
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
        title = _getTitleTagFromId3File(fileTags)
        artistName = _getArtistNameTagFromMutagenFile(fileTags)
        albumName = _getAlbumNameTagFromMutagenFile(fileTags)
        albumArtistsNameString = _getalbumArtistsNametringTagFromMutagenFile(fileTags)
        genreName = _getGenreNameTagFromMutagenFile(fileTags)
        rating = _getRatingTagFromMutagenFile(fileTags, appRatingMaxValue) 
        language = _getLanguageTagFromMutagenFile(fileTags) 

    elif fileExtension.lower() == ".flac":
        fileTags = FLAC(fileobj=file)
        title = _getTitleTagFromFlacFile(fileTags)
        artistName = _getArtistNameTagFromFlacFile(fileTags)
        albumName = _getAlbumNameTagFromFlacFile(fileTags)
        albumArtistsNameString = _getalbumArtistsNametringTagFromFlacFile(fileTags)
        genreName = _getGenreNameTagFromFlacFile(fileTags)
        rating = _getRatingTagFromFlacFile(fileTags, appRatingMaxValue) 
        language = _getLanguageTagFromFlacFile(fileTags)
    else:
        raise ValueError(FILE_EXTENSION_NOT_HANDLED_MESSAGE)
    
    metadataDict = dict()
    metadataDict[METADATA_DICT_TITLE_KEY] = title
    metadataDict[METADATA_DICT_ARTIST_NAME_KEY] = artistName
    metadataDict[METADATA_DICT_ALBUM_NAME_KEY] = albumName
    metadataDict[METADATA_DICT_ALBUM_ARTISTS_NAME_STRING_KEY] = albumArtistsNameString
    metadataDict[METADATA_DICT_GENRE_NAME_KEY] = genreName
    metadataDict[METADATA_DICT_DURATION_KEY] = _getDurationFromFileTags(fileTags=fileTags)
    metadataDict[METADATA_DICT_RATING_KEY] = rating
    metadataDict[METADATA_DICT_LANGUAGE_KEY] = language
    return metadataDict


def _getDurationFromFileTags(fileTags):
    return fileTags.info.length


def _getTitleTagFromId3File(id3FileTags: MutagenFile):
    return _getFirstValueIfExistsOrEmptyString(id3FileTags, ID3_TITLE_TEXT_FRAME)


def _getArtistNameTagFromMutagenFile(id3FileTags: MutagenFile):
    return _getFirstValueIfExistsOrEmptyString(id3FileTags, ID3_ARTIST_NAME_TEXT_FRAME)


def _getAlbumNameTagFromMutagenFile(id3FileTags: MutagenFile):
    return _getFirstValueIfExistsOrEmptyString(id3FileTags, ID3_ALBUM_NAME_TEXT_FRAME)


def _getalbumArtistsNametringTagFromMutagenFile(id3FileTags: MutagenFile):
    albumArtistsNameStringRaw = (
            _getFirstValueIfExistsOrEmptyString(id3FileTags, ID3_ALBUM_ARTISTS_NAMES_TEXT_FRAME))
    return albumArtistsNameStringRaw.strip()


def _getGenreNameTagFromMutagenFile(id3FileTags: MutagenFile):
    if ID3_GENRE_NAME_TEXT_FRAME in id3FileTags:
        return id3FileTags[ID3_GENRE_NAME_TEXT_FRAME][0]
    else:
        return ""


def _getEventuallyNormalizedRatingFromFileValue(
        fileRating: int, fileMaxRating: int=None, appMaxRating: int=None):
    if fileRating is not None:
        if appMaxRating is not None:
            if fileMaxRating is None:
                raise ValueError("normalizedMaxValue should be set as normalizedMaxValue is.")
            return _getNormalizedRatingFromFileValue(
                    ratingValue=fileRating, 
                    unnormalizedMaxValue=fileMaxRating,
                    normalizedMaxValue=appMaxRating)
        else:
            return fileRating
    else:
        return None
   

def _getRatingTagFromMutagenFile(id3FileTags: MutagenFile, appRatingMaxValue: int=None):
    fileRating = None
    for key in id3FileTags:
        if ID3_RATING_TEXT_FRAME in key:
            fileRating = id3FileTags[key].rating
            
    if fileRating is None:
        return None
    else:
        return _getEventuallyNormalizedRatingFromFileValue(
                fileRating=fileRating, 
                fileMaxRating=ID3_RATING_MAX_VALUE,
                appMaxRating=appRatingMaxValue)


def _getRatingTagFromFlacFile(flacFile: FLAC, appRatingMaxValue: int=None):
    fileRating = _getFirstValueIfExistsOrNone(flacFile, VORBIS_RATING_TAG_KEY)
    if fileRating is None or fileRating == "":
        return None
    else:
        return _getEventuallyNormalizedRatingFromFileValue(
                fileRating=fileRating, 
                fileMaxRating=VORBIS_RATING_MAX_VALUE,
                appMaxRating=appRatingMaxValue)


def _getNormalizedRatingFromFileValue(
            ratingValue: int, unnormalizedMaxValue: int, normalizedMaxValue: int):
    return int(round((ratingValue * normalizedMaxValue)/unnormalizedMaxValue))
    

def _getLanguageTagFromMutagenFile(id3FileTags: MutagenFile):
    return _getFirstValueIfExistsOrEmptyString(id3FileTags, ID3_LANGUAGE_TEXT_FRAME)


def _getTitleTagFromFlacFile(flacFileTags: FLAC):
    return _getFirstValueIfExistsOrEmptyString(flacFileTags, VORBIS_TITLE_TAG_KEY)


def _getArtistNameTagFromFlacFile(flacFileTags: FLAC):
    return _getFirstValueIfExistsOrEmptyString(flacFileTags, VORBIS_ARTIST_NAME_TAG_KEY)


def _getAlbumNameTagFromFlacFile(flacFileTags: FLAC):
    return _getFirstValueIfExistsOrEmptyString(flacFileTags, VORBIS_ALBUM_NAME_TAG_KEY)


def _getalbumArtistsNametringTagFromFlacFile(flacFileTags: FLAC):
    albumArtistsNameStringRaw = (
            _getFirstValueIfExistsOrEmptyString(
                    flacFileTags, VORBIS_ALBUM_ARTISTS_NAMES_TAG_KEY))
    return albumArtistsNameStringRaw.strip()


def _getGenreNameTagFromFlacFile(flacFileTags: FLAC):
    if VORBIS_GENRE_NAME_TAG_KEY in flacFileTags:
        return flacFileTags[VORBIS_GENRE_NAME_TAG_KEY][0]
    else:
        return ""
    

def _getLanguageTagFromFlacFile(flacFile: FLAC):
    return _getFirstValueIfExistsOrEmptyString(flacFile, VORBIS_LANGUAGE_TAG_KEY)


def _getSpecificMetadataFromId3File(
            id3FileTags: MutagenFile, metadataKey: str, normalizedRatingMaxValue: int=None):
    if metadataKey == METADATA_DICT_TITLE_KEY:
        return _getTitleTagFromId3File(id3FileTags)
    elif metadataKey == METADATA_DICT_ARTIST_NAME_KEY:
        return _getArtistNameTagFromMutagenFile(id3FileTags)
    elif metadataKey == METADATA_DICT_ALBUM_NAME_KEY:
        return _getAlbumNameTagFromMutagenFile(id3FileTags)
    elif metadataKey == METADATA_DICT_ALBUM_ARTISTS_NAME_STRING_KEY:
        return _getalbumArtistsNametringTagFromMutagenFile(id3FileTags)
    elif metadataKey == METADATA_DICT_GENRE_NAME_KEY:
        return _getGenreNameTagFromMutagenFile(id3FileTags)
    elif metadataKey == METADATA_DICT_DURATION_KEY:
        return _getDurationFromFileTags(id3FileTags)
    elif metadataKey == METADATA_DICT_RATING_KEY:
        return _getRatingTagFromMutagenFile(id3FileTags, normalizedRatingMaxValue)
    elif metadataKey == METADATA_DICT_LANGUAGE_KEY:
        return _getLanguageTagFromMutagenFile(id3FileTags)


def _getSpecificMetadataFromFlacFile(
        flacFileTags: FLAC, metadataKey: str, normalizedRatingMaxValue: int = None):
    if metadataKey == METADATA_DICT_TITLE_KEY:
        return _getTitleTagFromFlacFile(flacFileTags)
    elif metadataKey == METADATA_DICT_ARTIST_NAME_KEY:
        return _getArtistNameTagFromFlacFile(flacFileTags)
    elif metadataKey == METADATA_DICT_ALBUM_NAME_KEY:
        return _getAlbumNameTagFromFlacFile(flacFileTags)
    elif metadataKey == METADATA_DICT_ALBUM_ARTISTS_NAME_STRING_KEY:
        return _getalbumArtistsNametringTagFromFlacFile(flacFileTags)
    elif metadataKey == METADATA_DICT_GENRE_NAME_KEY:
        return _getGenreNameTagFromFlacFile(flacFileTags)
    elif metadataKey == METADATA_DICT_DURATION_KEY:
        return _getDurationFromFileTags(flacFileTags)
    elif metadataKey == METADATA_DICT_RATING_KEY:
        return _getRatingTagFromFlacFile(flacFileTags, normalizedRatingMaxValue)
    elif metadataKey == METADATA_DICT_LANGUAGE_KEY:
        return _getLanguageTagFromFlacFile(flacFileTags)


def _getId3FileTagsUpdatedIfTagValueSpecified(
        id3FileTags: ID3, 
        updateMetadataDict: dict, 
        updateMetadataKey: str, 
        appMaxRating: int):
    if updateMetadataKey in updateMetadataDict:
        if updateMetadataKey == METADATA_DICT_TITLE_KEY:
            id3Key = ID3_TITLE_TEXT_FRAME
            textFrameClass = TIT2
        elif updateMetadataKey == METADATA_DICT_ARTIST_NAME_KEY:
            id3Key = ID3_ARTIST_NAME_TEXT_FRAME
            textFrameClass = TPE1
        elif updateMetadataKey == METADATA_DICT_ALBUM_NAME_KEY:
            id3Key = ID3_ALBUM_NAME_TEXT_FRAME
            textFrameClass = TALB
        elif updateMetadataKey == METADATA_DICT_ALBUM_ARTISTS_NAME_STRING_KEY:
            id3Key = ID3_ALBUM_ARTISTS_NAMES_TEXT_FRAME
            textFrameClass = TPE2
        elif updateMetadataKey == METADATA_DICT_GENRE_NAME_KEY:
            id3Key = ID3_GENRE_NAME_TEXT_FRAME
            textFrameClass = TCON
        elif updateMetadataKey == METADATA_DICT_RATING_KEY:
            id3FileTags.delall(ID3_RATING_TEXT_FRAME)
            appRating = updateMetadataDict[METADATA_DICT_RATING_KEY]
            if appRating is not None:
                id3Rating = _getId3FileRatingFromAppValue(
                        appRating=appRating,
                        appMaxRating=appMaxRating)
                id3FileTags.add(POPM(email=ID3_RATING_APP_EMAIL, rating=id3Rating))
            return id3FileTags
        elif updateMetadataKey == METADATA_DICT_LANGUAGE_KEY:
            id3Key = ID3_LANGUAGE_TEXT_FRAME
            textFrameClass = TLAN
        else:
            raise KeyError(METADATA_DICT_UPDATE_KEY_NOT_HANDLED_MESSAGE)
        
        id3FileTags.delall(id3Key)
        id3FileTags.add(textFrameClass(encoding=3, text=updateMetadataDict[updateMetadataKey]))

    return id3FileTags


def _getId3FileRatingFromAppValue(appRating: int, appMaxRating: int):
    return _getFileRatingFromAppValue(
            appRating=appRating,
            appMaxRating=appMaxRating,
            fileMaxRating=ID3_RATING_MAX_VALUE)


def _getVorbisFileRatingFromAppValue(appRating: int, appMaxRating: int):
    return _getFileRatingFromAppValue(
            appRating=appRating,
            appMaxRating=appMaxRating,
            fileMaxRating=VORBIS_RATING_MAX_VALUE)


def _getFileRatingFromAppValue(appRating: int, appMaxRating: int, fileMaxRating: int):
    return int(round((fileMaxRating * appRating)/appMaxRating))


def _getFlacFileTagsUpdatedIfValueSpecified(
        flacFile: FLAC, metadataUpdateDict: dict, metadataDictKey: str):
    if metadataDictKey in metadataUpdateDict:
        if metadataDictKey == METADATA_DICT_TITLE_KEY:
            vorbisTagKey = VORBIS_TITLE_TAG_KEY
        elif metadataDictKey == METADATA_DICT_ARTIST_NAME_KEY:
            vorbisTagKey = VORBIS_ARTIST_NAME_TAG_KEY
        elif metadataDictKey == METADATA_DICT_ALBUM_NAME_KEY:
            vorbisTagKey = VORBIS_ALBUM_NAME_TAG_KEY
        elif metadataDictKey == METADATA_DICT_ALBUM_ARTISTS_NAME_STRING_KEY:
            vorbisTagKey = VORBIS_ALBUM_ARTISTS_NAMES_TAG_KEY
        elif metadataDictKey == METADATA_DICT_GENRE_NAME_KEY:
            flacFile[VORBIS_GENRE_NAME_TAG_KEY][0] = metadataUpdateDict[metadataDictKey]
            return flacFile
        elif metadataDictKey == METADATA_DICT_RATING_KEY:
            appRating = metadataUpdateDict[metadataDictKey]
            if appRating is not None:
                vorbisRating = _getVorbisFileRatingFromAppValue(
                        appRating=appRating, appMaxRating=VORBIS_RATING_MAX_VALUE)
                flacFile[VORBIS_RATING_TAG_KEY] = str(vorbisRating)
            else:
                flacFile[VORBIS_RATING_TAG_KEY] = ""
            return flacFile
        elif metadataDictKey == METADATA_DICT_LANGUAGE_KEY:
            vorbisTagKey = VORBIS_LANGUAGE_TAG_KEY
        else:
            raise KeyError(METADATA_DICT_UPDATE_KEY_NOT_HANDLED_MESSAGE)
        
        flacFile[vorbisTagKey] = metadataUpdateDict[metadataDictKey]

    return flacFile


def _getFirstValueIfExistsOrEmptyString(dict: dict, key: str):
    if key in dict:
        return dict[key][0]
    else:
        return ""


def _getFirstValueIfExistsOrNone(dict: dict, key: str):
    if key in dict:
        return int(dict[key][0])
    else:
        return None