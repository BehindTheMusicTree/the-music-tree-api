#!/usr/bin/env python
import os
import wave
import contextlib
from mutagen._file import File as MutagenFile
from mutagen.id3 import Frames
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.id3 import TIT2
from mutagen.id3 import TPE1
from mutagen.id3 import TALB
from mutagen.id3 import TPE2
from mutagen.id3 import TCON
from mutagen.id3 import POPM
from mutagen.id3 import TLAN
from mutagen.id3 import ID3NoHeaderError
from mutagen.mp3 import HeaderNotFoundError

TAG_ARTISTS_SEPARATION_CHAR = ","

# MP3 and Wave (.wav) files use ID3 tags
ID3_TITLE_TEXT_FRAME = 'TIT2'
ID3_ARTIST_NAME_TEXT_FRAME = 'TPE1'
ID3_ALBUM_NAME_TEXT_FRAME = 'TALB'
ID3_ALBUM_ARTISTS_NAMES_TEXT_FRAME = 'TPE2'
ID3_GENRE_NAME_TEXT_FRAME = 'TCON'
ID3_RATING_TEXT_FRAME = 'POPM'
ID3_RATING_APP_EMAIL = 'POPM:bodzify'
ID3_LANGUAGE_TEXT_FRAME = 'TLAN'

# FLAC files use Vorbis tags
VORBIS_TITLE_TAG_KEY = 'title'
VORBIS_ARTIST_NAME_TAG_KEY = 'artist'
VORBIS_ALBUM_NAME_TAG_KEY = 'album'
VORBIS_ALBUM_ARTISTS_NAMES_TAG_KEY = 'albumartist'
VORBIS_GENRE_NAME_TAG_KEY = 'genre'
VORBIS_RATING_TAG_KEY = 'rating'
VORBIS_LANGUAGE_TAG_KEY = 'language'

METADATA_DICT_TITLE_KEY = "title"
METADATA_DICT_ARTIST_NAME_KEY = "artistName"
METADATA_DICT_ALBUM_NAME_KEY = "albumName"
METADATA_DICT_ALBUM_ARTISTS_NAMES_STRING_KEY = "albumArtistsNamesString"
METADATA_DICT_GENRE_NAME_KEY = "genreName"
METADATA_DICT_DURATION_KEY = "duration"
METADATA_DICT_RATING_KEY = "rating"
METADATA_DICT_LANGUAGE_KEY = "language"

FILE_EXTENSION_NOT_HANDLED_MESSAGE = "The file's extension is not handled by the service."
METADATA_DICT_UPDATE_DURATION_SHOULDNT_BE_SET_MESSAGE = """The duration key has a value in the 
metadata dict. The duration cannot be updated. It is therefore ignored."""
METADATA_DICT_UPDATE_KEY_NOT_HANDLED_MESSAGE = """The specified audio metadata key is not 
handled by the service."""


def _getDurationFromId3File(filePath, fileExtensionLowered: str):
    if fileExtensionLowered == '.wav':
        return _getWaveFileDuration(filePath)
    else:
        return _getMp3FileDuration(filePath)


def _getWaveFileDuration(waveFilePath):
    with contextlib.closing(wave.open(waveFilePath,'r')) as file:
        return file.getnframes() / float(file.getframerate())


def _getMp3FileDuration(mp3Path: str):
        return MP3(mp3Path).info.length 


def _getTitleTagFromId3File(mutagenFile: MutagenFile):
    return _getFirstValueIfExistsOrEmptyString(mutagenFile, ID3_TITLE_TEXT_FRAME)


def _getArtistNameTagFromMutagenFile(mutagenFile: MutagenFile):
    return _getFirstValueIfExistsOrEmptyString(mutagenFile, ID3_ARTIST_NAME_TEXT_FRAME)


def _getAlbumNameTagFromMutagenFile(mutagenFile: MutagenFile):
    return _getFirstValueIfExistsOrEmptyString(mutagenFile, ID3_ALBUM_NAME_TEXT_FRAME)


def _getAlbumArtistsNameStringTagFromMutagenFile(mutagenFile: MutagenFile):
    albumArtistsNamesStringRaw = (
            _getFirstValueIfExistsOrEmptyString(mutagenFile, ID3_ALBUM_ARTISTS_NAMES_TEXT_FRAME))
    return albumArtistsNamesStringRaw.strip()


def _getGenreNameTagFromMutagenFile(mutagenFile: MutagenFile):
    if ID3_GENRE_NAME_TEXT_FRAME in mutagenFile:
        return mutagenFile[ID3_GENRE_NAME_TEXT_FRAME][0]
    else:
        return ""
   

def _getRatingTagFromMutagenFile(mutagenFile: MutagenFile):
    rating = 0
    for key in mutagenFile:
        if ID3_RATING_TEXT_FRAME in key:
            rating = mutagenFile[key].rating
    return rating
    

def _getLanguageTagFromMutagenFile(mutagenFile: MutagenFile):
    return _getFirstValueIfExistsOrEmptyString(mutagenFile, ID3_LANGUAGE_TEXT_FRAME)


def _getTitleTagFromFlacFile(flacFile: FLAC):
    return _getFirstValueIfExistsOrEmptyString(flacFile, VORBIS_TITLE_TAG_KEY)


def _getArtistNameTagFromFlacFile(flacFile: FLAC):
    return _getFirstValueIfExistsOrEmptyString(flacFile, VORBIS_ARTIST_NAME_TAG_KEY)


def _getAlbumNameTagFromFlacFile(flacFile: FLAC):
    return _getFirstValueIfExistsOrEmptyString(flacFile, VORBIS_ALBUM_NAME_TAG_KEY)


def _getAlbumArtistsNameStringTagFromFlacFile(flacFile: FLAC):
    albumArtistsNamesStringRaw = (
            _getFirstValueIfExistsOrEmptyString(flacFile, VORBIS_ALBUM_ARTISTS_NAMES_TAG_KEY))
    return albumArtistsNamesStringRaw.strip()


def _getGenreNameTagFromFlacFile(flacFile: FLAC):
    if VORBIS_GENRE_NAME_TAG_KEY in flacFile:
        return flacFile[VORBIS_GENRE_NAME_TAG_KEY][0]
    else:
        return ""


def _getDurationFromFlacFile(flacFile: FLAC):
    return flacFile.info.length
    

def _getRatingTagFromFlacFile(flacFile: FLAC):
    return _getFirstValueIfExistsOrZero(flacFile, VORBIS_RATING_TAG_KEY)
    

def _getLanguageTagFromFlacFile(flacFile: FLAC):
    return _getFirstValueIfExistsOrEmptyString(flacFile, VORBIS_LANGUAGE_TAG_KEY)


def _getSpecificMetadataFromId3File(
            id3File: ID3, metadataKey: str, filePath: str, fileExtensionLowered: str):
    if metadataKey == METADATA_DICT_TITLE_KEY:
        return _getTitleTagFromId3File(id3File)
    elif metadataKey == METADATA_DICT_ARTIST_NAME_KEY:
        return _getArtistNameTagFromMutagenFile(id3File)
    elif metadataKey == METADATA_DICT_ALBUM_NAME_KEY:
        return _getAlbumNameTagFromMutagenFile(id3File)
    elif metadataKey == METADATA_DICT_ALBUM_ARTISTS_NAMES_STRING_KEY:
        return _getAlbumArtistsNameStringTagFromMutagenFile(id3File)
    elif metadataKey == METADATA_DICT_GENRE_NAME_KEY:
        return _getGenreNameTagFromMutagenFile(id3File)
    elif metadataKey == METADATA_DICT_DURATION_KEY:
        _getDurationFromId3File(filePath=filePath, fileExtensionLowered=fileExtensionLowered)
    elif metadataKey == METADATA_DICT_RATING_KEY:
        return _getRatingTagFromMutagenFile(id3File)
    elif metadataKey == METADATA_DICT_LANGUAGE_KEY:
        return _getLanguageTagFromMutagenFile(id3File)


def _getSpecificMetadataFromFlacFile(flacFile: FLAC, metadataKey: str):
    if metadataKey == METADATA_DICT_TITLE_KEY:
        return _getTitleTagFromFlacFile(flacFile)
    elif metadataKey == METADATA_DICT_ARTIST_NAME_KEY:
        return _getArtistNameTagFromFlacFile(flacFile)
    elif metadataKey == METADATA_DICT_ALBUM_NAME_KEY:
        return _getAlbumNameTagFromFlacFile(flacFile)
    elif metadataKey == METADATA_DICT_ALBUM_ARTISTS_NAMES_STRING_KEY:
        return _getAlbumArtistsNameStringTagFromFlacFile(flacFile)
    elif metadataKey == METADATA_DICT_GENRE_NAME_KEY:
        return _getGenreNameTagFromFlacFile(flacFile)
    elif metadataKey == METADATA_DICT_DURATION_KEY:
        return _getDurationFromFlacFile(flacFile)
    elif metadataKey == METADATA_DICT_RATING_KEY:
        return _getRatingTagFromFlacFile(flacFile)
    elif metadataKey == METADATA_DICT_LANGUAGE_KEY:
        return _getLanguageTagFromFlacFile(flacFile)


def GetSpecificMetadataFromFile(file, metadataKey: str):
    filename, fileExtension = os.path.splitext(file.name)
    fileExtensionLowered = fileExtension.lower()
    if fileExtensionLowered in [".wav", ".mp3"]:
        mutagenFile = MutagenFile(file)
        return _getSpecificMetadataFromId3File(
                id3File=mutagenFile, 
                metadataKey=metadataKey,
                filePath=file.path,
                fileExtensionLowered=fileExtensionLowered)
    elif fileExtensionLowered == ".flac":
        flacFile = FLAC(fileobj=file)
        return _getSpecificMetadataFromFlacFile(flacFile=flacFile, metadataKey=metadataKey)    
    else:
        raise ValueError(FILE_EXTENSION_NOT_HANDLED_MESSAGE)
        

def GetMetadataDictFromFile(file):
    filename, fileExtension = os.path.splitext(file.name)

    title = ""
    artistName = ""
    albumName = ""
    albumArtistsNamesString = ""
    genreName = ""
    rating = 0 
    language = "" 
    
    fileExtensionLowered = fileExtension.lower()
    if fileExtensionLowered in [".wav", ".mp3"]:
        try:
            id3File = ID3(file)
            title = _getTitleTagFromId3File(id3File)
            artistName = _getArtistNameTagFromMutagenFile(id3File)
            albumName = _getAlbumNameTagFromMutagenFile(id3File)
            albumArtistsNamesString = _getAlbumArtistsNameStringTagFromMutagenFile(id3File)
            genreName = _getGenreNameTagFromMutagenFile(id3File)
            rating = _getRatingTagFromMutagenFile(id3File) 
            language = _getLanguageTagFromMutagenFile(id3File) 
        except HeaderNotFoundError:
            id3File = ID3()
            id3File.save(file)
        
        duration = _getDurationFromId3File(filePath=file , fileExtensionLowered=fileExtensionLowered)

    elif fileExtension.lower() == ".flac":
        trackFlacTags = FLAC(fileobj=file)
        title = _getTitleTagFromFlacFile(trackFlacTags)
        artistName = _getArtistNameTagFromFlacFile(trackFlacTags)
        albumName = _getAlbumArtistsNameStringTagFromFlacFile(trackFlacTags)
        albumArtistsNamesString = _getAlbumArtistsNameStringTagFromFlacFile(trackFlacTags)
        genreName = _getGenreNameTagFromFlacFile(trackFlacTags)
        duration = _getDurationFromFlacFile(trackFlacTags) 
        rating = _getRatingTagFromFlacFile(trackFlacTags) 
        language = _getLanguageTagFromFlacFile(trackFlacTags)
    
    else:
        raise ValueError(FILE_EXTENSION_NOT_HANDLED_MESSAGE)

    metadataDict = dict()
    metadataDict[METADATA_DICT_TITLE_KEY] = title
    metadataDict[METADATA_DICT_ARTIST_NAME_KEY] = artistName
    metadataDict[METADATA_DICT_ALBUM_NAME_KEY] = albumName
    metadataDict[METADATA_DICT_ALBUM_ARTISTS_NAMES_STRING_KEY] = albumArtistsNamesString
    metadataDict[METADATA_DICT_GENRE_NAME_KEY] = genreName
    metadataDict[METADATA_DICT_DURATION_KEY] = duration
    metadataDict[METADATA_DICT_RATING_KEY] = rating
    metadataDict[METADATA_DICT_LANGUAGE_KEY] = language
    return metadataDict


def _updateMutagenFileTagIfValueSet(id3: ID3, metadataDict: dict, metadataKey: str):
    if metadataKey in metadataDict:
        if metadataKey == METADATA_DICT_TITLE_KEY:
            id3Key = ID3_TITLE_TEXT_FRAME
            textFrameClass = TIT2
        elif metadataKey == METADATA_DICT_ARTIST_NAME_KEY:
            id3Key = ID3_ARTIST_NAME_TEXT_FRAME
            textFrameClass = TPE1
        elif metadataKey == METADATA_DICT_ALBUM_NAME_KEY:
            id3Key = ID3_ALBUM_NAME_TEXT_FRAME
            textFrameClass = TALB
        elif metadataKey == METADATA_DICT_ALBUM_ARTISTS_NAMES_STRING_KEY:
            id3Key = ID3_ALBUM_ARTISTS_NAMES_TEXT_FRAME
            textFrameClass = TPE2
        elif metadataKey == METADATA_DICT_GENRE_NAME_KEY:
            id3Key = ID3_GENRE_NAME_TEXT_FRAME
            textFrameClass = TCON
        elif metadataKey == METADATA_DICT_RATING_KEY:
            id3.delall(id3Key)
            id3.add(POPM(
                    email=ID3_RATING_APP_EMAIL, rating=metadataDict[METADATA_DICT_RATING_KEY]))
            return id3
        elif metadataKey == METADATA_DICT_LANGUAGE_KEY:
            id3Key = ID3_LANGUAGE_TEXT_FRAME
            textFrameClass = TLAN
        else:
            raise KeyError(METADATA_DICT_UPDATE_KEY_NOT_HANDLED_MESSAGE)
        
        id3.delall(id3Key)
        id3.add(textFrameClass(encoding=3, text=metadataDict[metadataKey]))

    return id3


def _updateFlacFileTagIfValueSet(flacFile: FLAC, metadataUpdateDict: dict, metadataDictKey: str):
    if metadataDictKey in metadataUpdateDict:
        if metadataDictKey == METADATA_DICT_TITLE_KEY:
            vorbisTagKey = VORBIS_TITLE_TAG_KEY
        elif metadataDictKey == METADATA_DICT_ARTIST_NAME_KEY:
            vorbisTagKey = VORBIS_ARTIST_NAME_TAG_KEY
        elif metadataDictKey == METADATA_DICT_ALBUM_NAME_KEY:
            vorbisTagKey = VORBIS_ALBUM_NAME_TAG_KEY
        elif metadataDictKey == METADATA_DICT_ALBUM_ARTISTS_NAMES_STRING_KEY:
            vorbisTagKey = VORBIS_ALBUM_ARTISTS_NAMES_TAG_KEY
        elif metadataDictKey == METADATA_DICT_GENRE_NAME_KEY:
            flacFile[VORBIS_GENRE_NAME_TAG_KEY][0] = metadataUpdateDict[metadataDictKey]
            return flacFile
        elif metadataDictKey == METADATA_DICT_RATING_KEY:
            flacFile[VORBIS_RATING_TAG_KEY] = str(metadataUpdateDict[metadataDictKey])
            return flacFile
        elif metadataDictKey == METADATA_DICT_LANGUAGE_KEY:
            vorbisTagKey = VORBIS_LANGUAGE_TAG_KEY
        else:
            raise KeyError(METADATA_DICT_UPDATE_KEY_NOT_HANDLED_MESSAGE)
        
        flacFile[vorbisTagKey] = metadataUpdateDict[metadataDictKey]

    return flacFile


def Update(file, metadataUpdateDict: dict):

    filename, fileExtension = os.path.splitext(file.name)
    fileExtensionLowered = fileExtension.lower()

    if fileExtensionLowered in [".wav", ".mp3"]:
        id3 = ID3(file.path)
        try:
            id3 = ID3(file.path)
        except ID3NoHeaderError:
            id3 = ID3()
        for metadataDictKey in list(metadataUpdateDict.keys()):
            if metadataDictKey == METADATA_DICT_DURATION_KEY:
                raise ValueError(METADATA_DICT_UPDATE_DURATION_SHOULDNT_BE_SET_MESSAGE)
            else:
                id3 = _updateMutagenFileTagIfValueSet(
                        id3=id3, 
                        metadataDict=metadataUpdateDict, 
                        metadataKey=metadataDictKey)
        id3.save(file.path)

    elif fileExtensionLowered == ".flac":
        flac = FLAC(file.path)
        for metadataDictKey in list(metadataUpdateDict.keys()):
            if metadataDictKey == METADATA_DICT_DURATION_KEY:
                raise ValueError(METADATA_DICT_UPDATE_DURATION_SHOULDNT_BE_SET_MESSAGE)
            else:
                flac = _updateFlacFileTagIfValueSet(
                        flacFile=flac, 
                        metadataUpdateDict=metadataUpdateDict, 
                        metadataDictKey=metadataDictKey)
        flac.save(file.path)
    else:
        raise ValueError(FILE_EXTENSION_NOT_HANDLED_MESSAGE)


def _getFirstValueIfExistsOrEmptyString(dict: dict, key: str):
    if key in dict:
        return dict[key][0]
    else:
        return ""


def _getFirstValueIfExistsOrZero(dict: dict, key: str):
    if key in dict:
        return int(dict[key][0])
    else:
        return 0