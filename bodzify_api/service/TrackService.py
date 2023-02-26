#!/usr/bin/env python
import os
from django.http.request import QueryDict
from django.contrib.auth.models import User
import bodzify_api.settings as settings
from bodzify_api.serializer.track.TrackSaveSerializer import TrackSaveSerializer
from bodzify_api.serializer.track.TrackPostSerializer import TrackPostSerializer
from bodzify_api.serializer.track.TrackSaveSchemaSerializer import TrackSaveSchemaSerializer
import bodzify_api.service.AudioMetadataService as AudioMetadataService
import bodzify_api.service.CriteriaService as CriteriaService
import bodzify_api.service.ArtistService as ArtistService
import bodzify_api.service.AlbumService as AlbumService
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.Criteria import CriteriaSpecialNames


def Save(user: User, requestData: QueryDict, oldTrack: LibraryTrack = None):
    saveData = _getSaveDataFromRequestData(user=user, requestData=requestData)
    saveData = _getSaveMutableDataWithDurationSetIfFileSet(saveMutableData=saveData)
    saveData[LibraryTrack.ATTRIBUTE_USER_LABEL] = user.id
    saveSerializer = TrackSaveSerializer(instance=oldTrack, data=saveData, partial=True)
    saveSerializer.is_valid(raise_exception=True)
    savedTrack = saveSerializer.save()

    _addTrackToGenresPlaylists(savedTrack)
    _updateTagsIfFileExists(savedTrack)

    return savedTrack


def CreateFromUpload(user: User, file):
    tagsDict = AudioMetadataService.GetMetadataDictFromFile(
            file=file, normalizedRatingMaxValue=settings.TRACK_RATING_MAX_VALUE)

    postSerializerData = dict()
    postSerializerData[LibraryTrack.ATTRIBUTE_USER_LABEL] = user.id
    postSerializerData[LibraryTrack.ATTRIBUTE_FILE_LABEL] = file

    title = tagsDict[AudioMetadataService.METADATA_DICT_TITLE_KEY]
    if title == "" or title is None:
        title, fileExtension = os.path.splitext(file.name)
    postSerializerData[LibraryTrack.ATTRIBUTE_TITLE_LABEL] = title
    
    artistName = tagsDict[AudioMetadataService.METADATA_DICT_ARTIST_NAME_KEY]
    if artistName is not None and artistName != "":
        artist = ArtistService.GetArtistFromNameAfterHavingEventuallyCreatedIt(
            user=user, artistName=artistName)
        postSerializerData[LibraryTrack.ATTRIBUTE_ARTIST_LABEL] = artist.uuid
    
    albumName = tagsDict[AudioMetadataService.METADATA_DICT_ALBUM_NAME_KEY]
    if albumName is not None and albumName != "":
        albumArtistsNamesString = tagsDict[AudioMetadataService.METADATA_DICT_ALBUM_ARTISTS_NAMES_STRING_KEY]
        if albumArtistsNamesString == "":
            albumArtistsNameList = None
        else:
            albumArtistsNameList = _getArtistsNameListFromString(albumArtistsNamesString)
        album = AlbumService.GetAlbumFromNameAndAlbumArtistsNamesAfterHavingEventuallyCreatedThem(
                user=user, albumName=albumName, albumArtistsNameList=albumArtistsNameList)
        postSerializerData[LibraryTrack.ATTRIBUTE_ALBUM_LABEL] = album.uuid
    
    genreName = tagsDict[AudioMetadataService.METADATA_DICT_GENRE_NAME_KEY]
    if genreName == "" or genreName is None:
        genreName = CriteriaSpecialNames.GENRE_GENRELESS
    genre = CriteriaService.GetCriteriaFromNameAfterHavingEventuallyCreatedIt(
        user=user, criteriaName=genreName)
    postSerializerData[LibraryTrack.ATTRIBUTE_GENRE_LABEL] = genre.uuid

    postSerializerData[LibraryTrack.ATTRIBUTE_DURATION_LABEL] = (
            tagsDict[AudioMetadataService.METADATA_DICT_DURATION_KEY])
    postSerializerData[LibraryTrack.ATTRIBUTE_RATING_LABEL] = (
            tagsDict[AudioMetadataService.METADATA_DICT_RATING_KEY])
    postSerializerData[LibraryTrack.ATTRIBUTE_LANGUAGE_LABEL] = (
            tagsDict[AudioMetadataService.METADATA_DICT_LANGUAGE_KEY])
    
    return _createFromPostSerializerData(serializerData=postSerializerData)


def _getSaveMutableDataWithDurationSetIfFileSet(saveMutableData: QueryDict):
    fileKey = LibraryTrack.ATTRIBUTE_FILE_LABEL
    if fileKey in saveMutableData:
        file = saveMutableData[fileKey]
        duration = AudioMetadataService.GetSpecificMetadataFromFile(
            file=file, metadataKey=AudioMetadataService.METADATA_DICT_DURATION_KEY)
        saveMutableData[LibraryTrack.ATTRIBUTE_DURATION_LABEL] = duration
    return saveMutableData


def _getSaveMutableDataWithAlbumUuidEventuallySet(
        user: User, requestData: QueryDict, saveMutableData: QueryDict):
    albumNameKey = TrackSaveSchemaSerializer.ATTRIBUTE_ALBUM_NAME_LABEL
    if albumNameKey in requestData:

        albumName = requestData[albumNameKey]

        artistsNamesKey = TrackSaveSchemaSerializer.ATTRIBUTE_ARTISTS_NAMES_LABEL
        if artistsNamesKey in requestData:
            albumArtistsNamesString = requestData[artistsNamesKey]
            albumArtistsNamesList = _getArtistsNameListFromString(albumArtistsNamesString)
        else:
            albumArtistsNamesList = None

        album = AlbumService.GetAlbumFromNameAndAlbumArtistsNamesAfterHavingEventuallyCreatedThem(
                user=user, albumName=albumName, albumArtistsNameList=albumArtistsNamesList)
        
        if album is not None:
            saveMutableData[albumNameKey] = album.uuid
        else:
            saveMutableData[albumNameKey] = None
    return saveMutableData


def _getSaveMutableDataWithArtistUuidEventuallySet(
        user: User, requestData: QueryDict, saveMutableData: QueryDict):
    artistNameKey = TrackSaveSchemaSerializer.ATTRIBUTE_ARTIST_NAME_LABEL
    if artistNameKey in requestData:
        artistName = requestData[artistNameKey]
        artist = ArtistService.GetArtistFromNameAfterHavingEventuallyCreatedIt(
                user=user, artistName=artistName)
        artistKey = LibraryTrack.ATTRIBUTE_ARTIST_LABEL
        if artist is not None:
            saveMutableData[artistKey] = artist.uuid
        else:
            saveMutableData[artistKey] = None
    return saveMutableData


def _getSaveMutableDataWithGenreUuidEventuallySet(
        user: User, requestData: QueryDict, saveMutableData: QueryDict):
    genreNameKey = TrackSaveSchemaSerializer.ATTRIBUTE_GENRE_NAME_LABEL
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


def _updateTagsIfFileExists(track: LibraryTrack):
    if track.fileExists == False:
        return
    
    metadataUpdateDict = dict()
    
    titleTag = track.title
    if titleTag is None:
        metadataUpdateDict = ""
    metadataUpdateDict[AudioMetadataService.METADATA_DICT_TITLE_KEY] = titleTag
    
    if track.artist_id is not None:
        artistNameTag = track.artist.name
    else:
        artistNameTag = ""
    metadataUpdateDict[AudioMetadataService.METADATA_DICT_ARTIST_NAME_KEY] = artistNameTag
    
    albumArtistsTag = ""
    if track.album_id is not None:
        albumNameTag = track.album.name

        albumArtistNamesIndex = 0
        for albumArtist in track.album.albumArtists.all():
            if albumArtistNamesIndex != 0:
                albumArtistsTag = (
                    albumArtistsTag + AudioMetadataService.TAG_ARTISTS_SEPARATION_CHAR)
            albumArtistsTag = albumArtistsTag + albumArtist.name
            albumArtistNamesIndex = albumArtistNamesIndex + 1
    else:
        albumNameTag = ""
        
    if albumNameTag is None:
        albumNameTag = ""
    metadataUpdateDict[AudioMetadataService.METADATA_DICT_ALBUM_NAME_KEY] = albumNameTag

    if track.genre.name is CriteriaSpecialNames.GENRE_GENRELESS:
        genreNameTag = ""
    else:
        genreNameTag = track.genre.name
    metadataUpdateDict[AudioMetadataService.METADATA_DICT_GENRE_NAME_KEY] = genreNameTag

    metadataUpdateDict[AudioMetadataService.METADATA_DICT_RATING_KEY] = track.rating

    languageTag = track.language
    if languageTag is None:
        languageTag = ""
    metadataUpdateDict[AudioMetadataService.METADATA_DICT_LANGUAGE_KEY] = languageTag

    AudioMetadataService.Update(
            file=track.file, 
            metadataUpdateDict=metadataUpdateDict, 
            appRatingMaxValue=settings.TRACK_RATING_MAX_VALUE)


def _createFromPostSerializerData(serializerData: QueryDict):
    postSerializer = TrackPostSerializer(data=serializerData)
    postSerializer.is_valid(raise_exception=True)
    track = postSerializer.save()
    _addTrackToGenresPlaylists(track)
    return track


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


def _getSaveDataFromRequestData(user: User, requestData: QueryDict) -> dict:
    saveMutableData = dict()
    
    saveMutableData = _getSaveMutableDataWithAttributeEventuallySet(
            attributeKey=LibraryTrack.ATTRIBUTE_FILE_LABEL, 
            requestData=requestData, 
            saveMutableData=saveMutableData)
    
    saveMutableData = _getSaveMutableDataWithAttributeEventuallySet(
            attributeKey=LibraryTrack.ATTRIBUTE_TITLE_LABEL, 
            requestData=requestData, 
            saveMutableData=saveMutableData)
    
    saveMutableData = _getSaveMutableDataWithArtistUuidEventuallySet(
            user=user, requestData=requestData, saveMutableData=saveMutableData)
    
    saveMutableData = _getSaveMutableDataWithAlbumUuidEventuallySet(
            user=user, requestData=requestData, saveMutableData=saveMutableData)
    
    saveMutableData = _getSaveMutableDataWithGenreUuidEventuallySet(
            user=user, requestData=requestData, saveMutableData=saveMutableData)
    
    saveMutableData = _getSaveMutableDataWithAttributeEventuallySet(
            attributeKey=LibraryTrack.ATTRIBUTE_RATING_LABEL, 
            requestData=requestData, 
            saveMutableData=saveMutableData)
    
    saveMutableData = _getSaveMutableDataWithAttributeEventuallySet(
            attributeKey=LibraryTrack.ATTRIBUTE_LANGUAGE_LABEL, 
            requestData=requestData, 
            saveMutableData=saveMutableData)
    
    return saveMutableData

def _getSaveMutableDataWithAttributeEventuallySet(
        attributeKey: str, requestData: QueryDict, saveMutableData: QueryDict):
    if attributeKey in requestData:
        saveMutableData[attributeKey] = requestData[attributeKey]
    return saveMutableData