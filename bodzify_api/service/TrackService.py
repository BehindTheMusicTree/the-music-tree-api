#!/usr/bin/env python
import os
from pathlib import Path
from django.core.files import File
from django.http.request import QueryDict
from django.contrib.auth.models import User
import bodzify_api.view.viewset.track.TrackViewSet as TrackViewSet
from bodzify_api.serializer.track.TrackPutSerializer import TrackPutSerializer
from bodzify_api.serializer.track.TrackPostSerializer import TrackPostSerializer
import bodzify_api.service.AudioMetadataService as AudioMetadataService
import bodzify_api.service.CriteriaService as CriteriaService
import bodzify_api.service.ArtistService as ArtistService
import bodzify_api.service.AlbumService as AlbumService
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.track.MineTrack import MineTrack
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.Criteria import CriteriaSpecialNames


def _setAlbumObjectFromNameAndAlbumArtistsNameInSerializerDataIfSet(
        user: User, mutableData: QueryDict):
    if TrackViewSet.DATA_ALBUM_NAME_PARAMETER_NAME in mutableData:

        albumName = mutableData[TrackViewSet.DATA_ALBUM_NAME_PARAMETER_NAME]

        if TrackViewSet.DATA_ALBUM_ARTISTS_NAMES_PARAMETER_NAME in mutableData:
            albumArtistsNamesString = mutableData[
                    TrackViewSet.DATA_ALBUM_ARTISTS_NAMES_PARAMETER_NAME]
            albumArtistsNamesList = _getArtistsNameListFromString(albumArtistsNamesString)
        else:
            albumArtistsNamesList = None

        album = AlbumService.GetAlbumFromNameAndAlbumArtistsNamesAfterHavingEventuallyCreatedThem(
                user=user, albumName=albumName, albumArtistsNameList=albumArtistsNamesList)
        
        if album is not None:
            mutableData[TrackViewSet.DATA_ALBUM_PARAMETER_NAME] = album.uuid
        else:
            mutableData[TrackViewSet.DATA_ALBUM_PARAMETER_NAME] = None


def _setArtistObjectFromNameInSerializerDataIfSet(user: User, mutableData: QueryDict):
    if TrackViewSet.DATA_ARTIST_NAME_PARAMETER_NAME in mutableData:
        artistName = mutableData[TrackViewSet.DATA_ARTIST_NAME_PARAMETER_NAME]
        artist = ArtistService.GetArtistFromNameAfterHavingEventuallyCreatedIt(
                user=user, artistName=artistName)
        if artist is not None:
            mutableData[TrackViewSet.DATA_ARTIST_PARAMETER_NAME] = artist.uuid
        else:
            mutableData[TrackViewSet.DATA_ARTIST_PARAMETER_NAME] = None


def _setGenreObjectInSerializerData(user: User, mutableData: QueryDict):
    if TrackViewSet.DATA_GENRE_PARAMETER_NAME in mutableData:
        if mutableData[TrackViewSet.DATA_GENRE_PARAMETER_NAME] is None:
            mutableData[TrackViewSet.DATA_GENRE_PARAMETER_NAME] = Criteria.objects.get(
                    user=user, name=CriteriaSpecialNames.GENRE_GENRELESS).uuid


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

    if track.genre is None:
        genreNameTag = ""
    else:
        genreNameTag = track.genre.name
    metadataUpdateDict[AudioMetadataService.METADATA_DICT_GENRE_NAME_KEY] = genreNameTag

    ratingTag = track.rating
    if ratingTag is None:
        ratingTag = 0
    metadataUpdateDict[AudioMetadataService.METADATA_DICT_RATING_KEY] = ratingTag

    languageTag = track.language
    if languageTag is None:
        languageTag = ""
    metadataUpdateDict[AudioMetadataService.METADATA_DICT_LANGUAGE_KEY] = languageTag

    AudioMetadataService.Update(file=track.file, metadataUpdateDict=metadataUpdateDict)


def CreateFromUpload(user: User, file):
    tagsDict = AudioMetadataService.GetMetadataDictFromFile(file)

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
    
    postSerializer = TrackPostSerializer(data=postSerializerData)
    postSerializer.is_valid(raise_exception=True)
    track = postSerializer.save()
    _addTrackToGenresPlaylists(user, track)
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

def _addTrackToGenresPlaylists(user: User, track: LibraryTrack):
    genre = track.genre
    while genre is not None:
        track.playlists.add(Playlist.objects.get(user=user, criteria=genre))
        genre = genre.parent
    track.save()

def _getSerializerDataFromRequestData(user: User, requestData: QueryDict) -> dict:
    serializerData = requestData.copy()
    serializerData = _setGenreObjectInSerializerData(user, serializerData)
    serializerData = _setArtistObjectFromNameInSerializerDataIfSet(user, serializerData)
    serializerData = _setAlbumObjectFromNameAndAlbumArtistsNameInSerializerDataIfSet(user, serializerData)


def Update(user: User, oldTrack: LibraryTrack, requestData: QueryDict):
    putSerializerData = _getSerializerDataFromRequestData(user, requestData)
    putSerializer = TrackPutSerializer(instance=oldTrack, data=putSerializerData, partial=True)
    putSerializer.is_valid(raise_exception=True)
    updatedTrack = putSerializer.save()

    _addTrackToGenresPlaylists(user=user, track=updatedTrack)
    _updateTagsIfFileExists(updatedTrack)

    return updatedTrack


def CreateFromMineExtract(user: User, requestData: QueryDict, trackTempFileAbsPath: str):    
    path = Path(trackTempFileAbsPath)
    file = path.open(mode='rb')

    postSerializerData = _getSerializerDataFromRequestData(user, requestData)
    postSerializerData[LibraryTrack.ATTRIBUTE_USER_LABEL] = user.id
    postSerializerData[LibraryTrack.ATTRIBUTE_FILE_LABEL] = File(file, name=path.name)
    postSerializerData[LibraryTrack.ATTRIBUTE_DURATION_LABEL] = (
        AudioMetadataService.GetSpecificMetadataFromFile(
                file=trackTempFileAbsPath, 
                metadataKey=AudioMetadataService.METADATA_DICT_DURATION_KEY)
    )

    postSerializer = TrackPostSerializer(data=postSerializerData)
    postSerializer.is_valid(raise_exception=True)
    track = postSerializer.save()
    _addTrackToGenresPlaylists(user=user, track=track)
    _updateTagsIfFileExists(track=track)

    return track
