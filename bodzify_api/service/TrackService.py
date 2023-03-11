#!/usr/bin/env python
import os
from django.http.request import QueryDict
from django.contrib.auth.models import User
from bodzify_api.serializer.track.input.TrackPostSchemaSerializer import TrackPostSchemaSerializer
import bodzify_api.settings as settings
from bodzify_api.serializer.track.input.TrackSaveSerializer import TrackSaveSerializer
from bodzify_api.serializer.track.input.TrackUpdateSchemaSerializer import TrackUpdateSchemaSerializer
import bodzify_api.service.AudioMetadataService as AudioMetadataService
import bodzify_api.service.CriteriaService as CriteriaService
import bodzify_api.service.ArtistService as ArtistService
import bodzify_api.service.AlbumService as AlbumService
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.Criteria import CriteriaSpecialNames


def Create(user: User, postSchemaData: QueryDict):
    serializer = TrackPostSchemaSerializer(data=postSchemaData)
    serializer.is_valid(raise_exception=True)
    return Save(user=user, saveSchemaData=postSchemaData)
    
    
def Update(user: User, updateSchemaData: QueryDict, oldTrack: LibraryTrack):
    serializer = TrackUpdateSchemaSerializer(data=updateSchemaData)
    serializer.is_valid(raise_exception=True)
    return Save(user=user, saveSchemaData=updateSchemaData, oldTrack=oldTrack)


def Save(user: User, saveSchemaData: QueryDict, oldTrack: LibraryTrack=None):
    
    fileKey = LibraryTrack.ATTRIBUTE_FILE_LABEL
    saveDataFromFile = dict()
    if fileKey in saveSchemaData:
        file = saveSchemaData[fileKey]
        if file is not None and file != "":
            saveDataFromFile = _getSaveDataFromFile(user=user, file=file)
        
    saveData = _getSaveDataOverridenWithInputData(
            user=user, saveData=saveDataFromFile, inputData=saveSchemaData)
    saveData[LibraryTrack.ATTRIBUTE_USER_LABEL] = user.id
    
    if oldTrack is None:    
        titleKey = LibraryTrack.ATTRIBUTE_TITLE_LABEL
        if titleKey in saveData:
            if saveData[titleKey] is None:
                saveData[titleKey], extension = os.path.splitext(file.name)
                        
    saveSerializer = TrackSaveSerializer(instance=oldTrack, data=saveData, partial=True)
    saveSerializer.is_valid(raise_exception=True)
    savedTrack = saveSerializer.save()

    _addTrackToGenresPlaylists(savedTrack)
    _updateFileTagsIfFileExists(savedTrack)

    return savedTrack


def _getSaveDataFromFile(user:User, file):
    metadata = AudioMetadataService.GetMetadataDictFromFile(
            file=file, normalizedRatingMaxValue=settings.TRACK_RATING_MAX_VALUE)

    saveData = dict()
    saveData[LibraryTrack.ATTRIBUTE_USER_LABEL] = user.id
    saveData[LibraryTrack.ATTRIBUTE_FILE_LABEL] = file

    title = metadata[AudioMetadataService.METADATA_DICT_KEYS.TITLE]
    if title == "" or title is None:
        title, fileExtension = os.path.splitext(file.name)
    saveData[LibraryTrack.ATTRIBUTE_TITLE_LABEL] = title
    
    artistName = metadata[AudioMetadataService.METADATA_DICT_KEYS.ARTIST_NAME]
    if artistName is not None and artistName != "":
        artist = ArtistService.GetArtistFromNameAfterEventualCreation(
                user=user, artistName=artistName)
        saveData[LibraryTrack.ATTRIBUTE_ARTIST_LABEL] = artist.uuid
    
    albumName = metadata[AudioMetadataService.METADATA_DICT_KEYS.ALBUM_NAME]
    if albumName is not None and albumName != "":
        albumArtistsNameKey = AudioMetadataService.METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES
        albumArtistsNameString = metadata[albumArtistsNameKey]
        if albumArtistsNameString == "":
            albumArtistsNameList = None
        else:
            albumArtistsNameList = _getArtistsNameListFromString(albumArtistsNameString)
        album = AlbumService.GetAlbumFromNameAndalbumArtistsNameAfterEventualCreations(
                user=user, albumName=albumName, albumArtistsNameList=albumArtistsNameList)
        saveData[LibraryTrack.ATTRIBUTE_ALBUM_LABEL] = album.uuid
    
    genreName = metadata[AudioMetadataService.METADATA_DICT_KEYS.GENRE_NAME]
    if genreName == "" or genreName is None:
        genreName = CriteriaSpecialNames.GENRE_GENRELESS
    genre = CriteriaService.GetCriteriaFromNameAfterHavingEventuallyCreatedIt(
        user=user, criteriaName=genreName)
    saveData[LibraryTrack.ATTRIBUTE_GENRE_LABEL] = genre.uuid

    saveData[LibraryTrack.ATTRIBUTE_DURATION_LABEL] = (
            metadata[AudioMetadataService.METADATA_DICT_KEYS.DURATION])
    saveData[LibraryTrack.ATTRIBUTE_RATING_LABEL] = (
            metadata[AudioMetadataService.METADATA_DICT_KEYS.RATING])
    saveData[LibraryTrack.ATTRIBUTE_LANGUAGE_LABEL] = (
            metadata[AudioMetadataService.METADATA_DICT_KEYS.LANGUAGE])
    return saveData


def _getSaveMutableDataWithAlbumUuidIfAlbumNameInRequest(
        user: User, requestData: QueryDict, saveMutableData: QueryDict):
    albumNameKey = TrackUpdateSchemaSerializer.ATTRIBUTE_ALBUM_NAME_LABEL
    if albumNameKey in requestData:

        albumName = requestData[albumNameKey]

        artistsNamesKey = TrackUpdateSchemaSerializer.ATTRIBUTE_ALBUM_ARTISTS_NAMES_LABEL
        if artistsNamesKey in requestData:
            albumArtistsNameString = requestData[artistsNamesKey]
            albumArtistsNameList = _getArtistsNameListFromString(albumArtistsNameString)
        else:
            albumArtistsNameList = None

        album = AlbumService.GetAlbumFromNameAndalbumArtistsNameAfterEventualCreations(
                user=user, albumName=albumName, albumArtistsNameList=albumArtistsNameList)
        
        albumKey = LibraryTrack.ATTRIBUTE_ALBUM_LABEL 
        if album is not None:
            saveMutableData[albumKey] = album.uuid
        else:
            saveMutableData[albumKey] = None
    return saveMutableData


def _getSaveMutableDataWithArtistUuidIfSetInRequest(
        user: User, requestData: QueryDict, saveMutableData: QueryDict):
    artistNameKey = TrackUpdateSchemaSerializer.ATTRIBUTE_ARTIST_NAME_LABEL
    if artistNameKey in requestData:
        artistName = requestData[artistNameKey]
        artist = ArtistService.GetArtistFromNameAfterEventualCreation(
                user=user, artistName=artistName)
        artistKey = LibraryTrack.ATTRIBUTE_ARTIST_LABEL
        if artist is not None:
            saveMutableData[artistKey] = artist.uuid
        else:
            saveMutableData[artistKey] = None
    return saveMutableData


def _getSaveMutableDataWithGenreUuidIfSetInRequest(
        user: User, requestData: QueryDict, saveMutableData: QueryDict):
    genreNameKey = TrackUpdateSchemaSerializer.ATTRIBUTE_GENRE_NAME_LABEL
    if genreNameKey in requestData:
        genreName = requestData[genreNameKey]
        if genreName is None:
            genreUuid = Criteria.objects.get(
                    user=user, name=CriteriaSpecialNames.GENRE_GENRELESS).uuid
        else:
            genreUuid = CriteriaService.GetCriteriaFromNameAfterHavingEventuallyCreatedIt(
                    user=user, criteriaName=genreName).uuid
        saveMutableData[LibraryTrack.ATTRIBUTE_GENRE_LABEL] = genreUuid
    return saveMutableData


def _updateFileTagsIfFileExists(track: LibraryTrack):
    if track.fileExists == False:
        return
    
    metadataUpdateDict = dict()
    
    titleTag = track.title
    if titleTag is None:
        metadataUpdateDict = ""
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

    if track.genre.name is CriteriaSpecialNames.GENRE_GENRELESS:
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
        track.playlists.add(Playlist.objects.get(user=track.user, criteria=genre))
        genre = genre.parent
    track.save()


def _getSaveDataOverridenWithInputData(
        user: User, saveData: QueryDict, inputData: QueryDict) -> dict:
    saveMutableData = saveData.copy()
    
    saveMutableData = _getSaveMutableDataWithAttributeEventuallySetInRequestData(
            attributeKey=LibraryTrack.ATTRIBUTE_FILE_LABEL, 
            requestData=inputData, 
            saveMutableData=saveMutableData)
    
    saveMutableData = _getSaveMutableDataWithAttributeEventuallySetInRequestData(
            attributeKey=LibraryTrack.ATTRIBUTE_TITLE_LABEL, 
            requestData=inputData, 
            saveMutableData=saveMutableData)
    
    saveMutableData = _getSaveMutableDataWithArtistUuidIfSetInRequest(
            user=user, requestData=inputData, saveMutableData=saveMutableData)
    
    saveMutableData = _getSaveMutableDataWithAlbumUuidIfAlbumNameInRequest(
            user=user, requestData=inputData, saveMutableData=saveMutableData)
    
    saveMutableData = _getSaveMutableDataWithGenreUuidIfSetInRequest(
            user=user, requestData=inputData, saveMutableData=saveMutableData)
    
    saveMutableData = _getSaveMutableDataWithAttributeEventuallySetInRequestData(
            attributeKey=LibraryTrack.ATTRIBUTE_RATING_LABEL, 
            requestData=inputData, 
            saveMutableData=saveMutableData)
    
    saveMutableData = _getSaveMutableDataWithAttributeEventuallySetInRequestData(
            attributeKey=LibraryTrack.ATTRIBUTE_LANGUAGE_LABEL, 
            requestData=inputData, 
            saveMutableData=saveMutableData)
    
    return saveMutableData


def _getSaveMutableDataWithAttributeEventuallySetInRequestData(
        attributeKey: str, saveMutableData: QueryDict, requestData: QueryDict):
    if attributeKey in requestData:
        saveMutableData[attributeKey] = requestData[attributeKey]
    return saveMutableData
