#!/usr/bin/env python
import os
import random
import string
import requests
from tempfile import NamedTemporaryFile
from django.http.request import QueryDict
from django.contrib.auth.models import User
from django.core.files.base import File
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.model.playlist.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.track.MineTrack import ATTRIBUTES_LABEL as MINE_TRACK_ATTRIBUTES_LABEL
from bodzify_api.serializer.track.input.schema.TrackSaveSchemaSerializer import \
    ATTRIBUTES_LABEL as TRACK_SCHEMA_ATTRIBUTES_LABEL
from bodzify_api.serializer.track.input.schema.TrackPostSchemaSerializer import \
    TrackPostSchemaSerializer
from bodzify_api.service.criteria.GenreService import GenreService
import bodzify_api.settings as settings
from bodzify_api.serializer.track.input.TrackSaveModelSerializer import TrackSaveModelSerializer
from bodzify_api.serializer.track.input.schema.TrackUpdateSchemaSerializer import \
    TrackUpdateSchemaSerializer
import bodzify_api.service.AudioMetadataService as AudioMetadataService
import bodzify_api.service.ArtistService as ArtistService
import bodzify_api.service.AlbumService as AlbumService
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.track.LibraryTrack import ATTRIBUTES_LABEL as TRACK_ATTRIBUTES_LABEL
from bodzify_api.model.playlist.Playlist import Playlist


def Extract(user: User, extractSchemaData: QueryDict):
    mineTrackUrlLabel = extractSchemaData[MINE_TRACK_ATTRIBUTES_LABEL.URL]
    trackInMemoryFile = requests.get(mineTrackUrlLabel, stream=True)
    with NamedTemporaryFile(delete=True) as trackTempFile:
        for block in trackInMemoryFile.iter_content(1024 * 8):
            if not block:
                break
            trackTempFile.write(block)
        trackTempFile.flush()
        trackTempFile.seek(0)

        postSchemaData = _getSaveDataFromRequestData(extractSchemaData)

        trackFileName, isFilenameRandomlyGenerated = _getTrackFilenameWithExtension(
            mineTrackUrlLabel, extractSchemaData)
        postSchemaData[TRACK_ATTRIBUTES_LABEL.FILE] = File(
            trackTempFile, name=trackFileName)
        libraryTrack = Create(user=user, postSchemaData=postSchemaData,
                              forceTitleGeneration=isFilenameRandomlyGenerated)

    return libraryTrack


def Create(user: User, postSchemaData: QueryDict, forceTitleGeneration: bool=False):
    serializer = TrackPostSchemaSerializer(data=postSchemaData)
    serializer.is_valid(raise_exception=True)

    file = postSchemaData[TRACK_ATTRIBUTES_LABEL.FILE]
    saveSchemaDataFromFile = _getSaveSchemaDataFromFile(file=file)
    saveSchemaData = _getDict1OverridenWithDict2WhenKeyIsProvided(
        dict1=saveSchemaDataFromFile, dict2=postSchemaData)
    saveSchemaData[TRACK_ATTRIBUTES_LABEL.USER] = user.id

    if TRACK_ATTRIBUTES_LABEL.TITLE not in saveSchemaData:
        filename = os.path.basename(file.name).split('.')[0]
        if len(filename) > settings.TRACK_FILENAME_MAX_CHAR or forceTitleGeneration:
            title = settings.TRACK_GENERATED_TITLE_PREFIXE + \
                _generateShortUu(settings.TRACK_GENERATED_TITLE_LEN -
                                 len(settings.TRACK_GENERATED_TITLE_PREFIXE))
        else:
            title = filename
        saveSchemaData[TRACK_ATTRIBUTES_LABEL.TITLE] = title

    return Save(user=user, saveSchemaData=saveSchemaData)


def Update(user: User, updateSchemaData: QueryDict, oldTrack: LibraryTrack):
    serializer = TrackUpdateSchemaSerializer(data=updateSchemaData)
    serializer.is_valid(raise_exception=True)
    return Save(user=user, saveSchemaData=updateSchemaData, oldTrack=oldTrack)


def Save(user: User, saveSchemaData: QueryDict, oldTrack: LibraryTrack = None):
    saveModelData = _getSaveModelDataFromSaveSchemaData(user=user, saveSchemaData=saveSchemaData)
    saveModelData[TRACK_ATTRIBUTES_LABEL.USER] = user.id
    saveSerializer = TrackSaveModelSerializer(instance=oldTrack, data=saveModelData, partial=True)
    saveSerializer.is_valid(raise_exception=True)
    savedTrack = saveSerializer.save()

    _addTrackToGenresPlaylists(savedTrack)
    _updateFileTagsIfFileExists(savedTrack)

    return savedTrack


def _getSaveSchemaDataFromFile(file):
    metadataDict = AudioMetadataService.GetMetadataDictFromFile(
        file=file, normalizedRatingMaxValue=settings.TRACK_RATING_MAX_VALUE)

    saveData = _removeNoneOrEmptyKeyFromDict(metadataDict)
    saveData[TRACK_ATTRIBUTES_LABEL.FILE] = file

    return saveData


def _removeNoneOrEmptyKeyFromDict(dict):
    for key in list(dict.keys()):
        if dict[key] is None or dict[key] == "":
            del dict[key]
    return dict


def _getDict1UpdatedWithArtistUuidIfArtistNameInDict2(
        user: User, dict1: QueryDict, dict2: QueryDict):
    artistNameKey = TRACK_SCHEMA_ATTRIBUTES_LABEL.ARTIST_NAME
    if artistNameKey in dict2:
        artistName = dict2[artistNameKey]
        artist = ArtistService.GetArtistFromNameAfterEventualCreation(
            user=user, artistName=artistName)
        artistKey = TRACK_ATTRIBUTES_LABEL.ARTIST
        if artist is not None:
            dict1[artistKey] = artist.uuid
        else:
            dict1[artistKey] = None
    return dict1


def _getDict1UpdatedWithAlbumUuidIfAlbumNameInDict2(
        user: User, dict1: QueryDict, dict2: QueryDict):
    albumNameKey = TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME

    if albumNameKey in dict2:
        albumName = dict2[albumNameKey]

        artistsNamesKey = TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAME_STRING
        if artistsNamesKey in dict2:
            albumArtistsNameString = dict2[artistsNamesKey]
            if albumArtistsNameString is not None:
                albumArtistsNameList = _getArtistsNameListFromString(
                    albumArtistsNameString)
            else:
                albumArtistsNameList = None
        else:
            albumArtistsNameList = None
        album = AlbumService.GetAlbumFromNameAndAlbumArtistsNameListAfterEventualCreations(
            user=user, albumName=albumName, albumArtistsNameList=albumArtistsNameList)

        albumKey = TRACK_ATTRIBUTES_LABEL.ALBUM
        if album is not None:
            dict1[albumKey] = album.uuid
        else:
            dict1[albumKey] = None
    return dict1


def _getDict1UpdatedWithGenreUuidIfGenreNameInDict2(
        user: User, dict1: QueryDict, dict2: QueryDict):
    genreNameKey = TRACK_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME
    if genreNameKey in dict2:
        genreName = dict2[genreNameKey]

        if genreName in ["", None]:
            genreUuid = None
        else:
            genreService = GenreService()
            genreUuid = genreService.getCriteriaFromNameAfterHavingEventuallyCreatedIt(
                user=user, criteriaName=genreName).uuid
        dict1[TRACK_ATTRIBUTES_LABEL.GENRE] = genreUuid
    return dict1


def _updateFileTagsIfFileExists(track: LibraryTrack):
    if track.fileExists == False:
        return

    metadataUpdateDict = dict()

    titleTag = track.title
    if titleTag is None:
        titleTag = ""
    metadataUpdateDict[AudioMetadataService.METADATA_DICT_KEYS.TITLE] = titleTag

    if track.artist_id is not None:
        artistNameTag = track.artist.name
    else:
        artistNameTag = ""
    metadataUpdateDict[AudioMetadataService.METADATA_DICT_KEYS.ARTIST_NAME] = artistNameTag

    albumArtistsTag = ""
    if track.album_id is not None:
        albumNameTag = track.album.name
        albumArtistsNameIndex = 0
        for albumArtist in list(track.album.albumArtists.all()):
            if albumArtistsNameIndex != 0:
                albumArtistsTag = (
                    albumArtistsTag + AudioMetadataService.TAG_ARTISTS_SEPARATION_CHAR)
            albumArtistsTag = albumArtistsTag + albumArtist.name
            albumArtistsNameIndex = albumArtistsNameIndex + 1
    else:
        albumNameTag = ""

    if albumNameTag is None:
        albumNameTag = ""
    metadataUpdateDict[AudioMetadataService.METADATA_DICT_KEYS.ALBUM_NAME] = albumNameTag
    albumArtistsNameKey = AudioMetadataService.METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES
    metadataUpdateDict[albumArtistsNameKey] = albumArtistsTag

    if track.genre == None:
        genreNameTag = ""
    else:
        genreNameTag = track.genre.name
    metadataUpdateDict[AudioMetadataService.METADATA_DICT_KEYS.GENRE_NAME] = genreNameTag

    metadataUpdateDict[AudioMetadataService.METADATA_DICT_KEYS.RATING] = track.rating

    languageTag = track.language
    if languageTag is None:
        languageTag = ""
    metadataUpdateDict[AudioMetadataService.METADATA_DICT_KEYS.LANGUAGE] = languageTag

    AudioMetadataService.Update(
        file=track.file,
        metadataUpdateDict=metadataUpdateDict,
        normalizedRatingMaxValue=settings.TRACK_RATING_MAX_VALUE)


def _getArtistsNameListFromString(namesString: str) -> list:
    namesWithEventualSpacesAroundAndDuplicates = namesString.split(
        AudioMetadataService.TAG_ARTISTS_SEPARATION_CHAR)
    names = list()
    for nameWithEventualSpacesAround in namesWithEventualSpacesAroundAndDuplicates:
        name = nameWithEventualSpacesAround.strip()
        if name != "" and names.count(name) == 0:
            names.append(name)
    return names


def _addTrackToGenresPlaylists(track: LibraryTrack):
    genre = track.genre
    while genre is not None:
        track.playlists.add(CriteriaPlaylist.objects.get(
            user=track.user, type=CriteriaTypesId.GENRE, criteria=genre))
        genre = genre.parent
    track.save()


def _getDict1OverridenWithDict2WhenKeyIsProvided(dict1: QueryDict, dict2: QueryDict) -> dict:
    overridenDict1 = dict1.copy()
    for key in [TRACK_ATTRIBUTES_LABEL.FILE,
                TRACK_ATTRIBUTES_LABEL.TITLE,
                TRACK_SCHEMA_ATTRIBUTES_LABEL.ARTIST_NAME,
                TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME,
                TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAME_STRING,
                TRACK_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME,
                TRACK_ATTRIBUTES_LABEL.RATING,
                TRACK_ATTRIBUTES_LABEL.LANGUAGE]:
        overridenDict1 = _getDict1UpdatedWithDict2KeyIfSet(
            key=key,
            dict1=overridenDict1,
            dict2=dict2)
    return overridenDict1


def _getSaveModelDataFromSaveSchemaData(user: User, saveSchemaData: QueryDict) -> dict:
    saveModelData = dict()

    saveModelData = _getDict1UpdatedWithDict2KeyIfSet(
        key=TRACK_ATTRIBUTES_LABEL.FILE,
        dict1=saveModelData,
        dict2=saveSchemaData)

    saveModelData = _getDict1UpdatedWithDict2KeyIfSet(
        key=TRACK_ATTRIBUTES_LABEL.TITLE,
        dict1=saveModelData,
        dict2=saveSchemaData)

    saveModelData = _getDict1UpdatedWithArtistUuidIfArtistNameInDict2(
        user=user, dict1=saveModelData, dict2=saveSchemaData)

    saveModelData = _getDict1UpdatedWithAlbumUuidIfAlbumNameInDict2(
        user=user, dict1=saveModelData, dict2=saveSchemaData)

    saveModelData = _getDict1UpdatedWithGenreUuidIfGenreNameInDict2(
        user=user, dict1=saveModelData, dict2=saveSchemaData)

    saveModelData = _getDict1UpdatedWithDict2KeyIfSet(
        key=TRACK_ATTRIBUTES_LABEL.DURATION,
        dict1=saveModelData,
        dict2=saveSchemaData)

    saveModelData = _getDict1UpdatedWithDict2KeyIfSet(
        key=TRACK_ATTRIBUTES_LABEL.RATING,
        dict1=saveModelData,
        dict2=saveSchemaData)

    saveModelData = _getDict1UpdatedWithDict2KeyIfSet(
        key=TRACK_ATTRIBUTES_LABEL.LANGUAGE,
        dict1=saveModelData,
        dict2=saveSchemaData)

    return saveModelData


def _getDict1UpdatedWithDict2KeyIfSet(
        key: str, dict1: QueryDict, dict2: QueryDict):
    if key in dict2:
        value = dict2[key]
        if value == "":
            value = None
        dict1[key] = value
    return dict1


def _getSaveDataFromRequestData(requestData: QueryDict):
    saveData = requestData.copy()
    del saveData[MINE_TRACK_ATTRIBUTES_LABEL.URL]
    return saveData


def _getFileExtensionFromUrl(url: str):
    return url.split(".")[-1]


def _getSubstringAfterLastSlash(string: str):
    return string.split("/")[-1]


def _getTrackFilenameWithExtension(mineTrackUrl: str, requestData: QueryDict):
    fileExtension = _getFileExtensionFromUrl(mineTrackUrl)
    isFilenameRandomlyGenerated = False
    titleKey = TRACK_ATTRIBUTES_LABEL.TITLE
    if titleKey in requestData:
        title = requestData[titleKey]
        artistNameKey = TRACK_SCHEMA_ATTRIBUTES_LABEL.ARTIST_NAME
        if artistNameKey in requestData:
            artistName = requestData[artistNameKey]
            if artistName is None or artistName == "":
                fileNameWithoutExtension = title
            else:
                fileNameWithoutExtension = artistName + " - " + title
        else:
            fileNameWithoutExtension = title
        filenameWithExtension = fileNameWithoutExtension + "." + fileExtension
    else:
        filenameWithExtension = _getSubstringAfterLastSlash(mineTrackUrl)
        if len(filenameWithExtension) > settings.TRACK_FILENAME_MAX_CHAR:
            fileNameWithoutExtension = _generateShortUu(
                settings.TRACK_FILENAME_GENERATED_WITHOUT_EXTENSION_LEN - len(fileExtension) - 1)
            filenameWithExtension = fileNameWithoutExtension + "." + fileExtension
            isFilenameRandomlyGenerated = True
    return filenameWithExtension, isFilenameRandomlyGenerated


def _generateShortUu(length: int):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
