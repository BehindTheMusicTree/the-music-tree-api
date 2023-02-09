#!/usr/bin/env python

import os
from pathlib import Path

from django.core.files import File
from django.http.request import QueryDict
from django.contrib.auth.models import User

from mutagen._file import File as MutagenFile
from mutagen.id3 import Frames
from mutagen.flac import FLAC
from mutagen.id3 import ID3
from mutagen.id3 import TIT2
from mutagen.id3 import POPM

import bodzify_api.view.viewset.track.LibraryTrackViewSet as LibraryTrackViewSet
import bodzify_api.service.CriteriaService as CriteriaService
import bodzify_api.service.ArtistService as ArtistService
import bodzify_api.service.PlaylistService as PlaylistService
import bodzify_api.service.AlbumService as AlbumService
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.track.MineTrack import MineTrack
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.Playlist import PlaylistSpecialNames
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.Criteria import CriteriaSpecialNames

TAG_ARTISTS_SEPARATION_CHAR = ","

# MP3 and Wave (.wav) files use ID3 tags
ID3_TITLE_TAG = 'TIT2'
ID3_ARTIST_TAG = 'TPE1'
ID3_ALBUM_TAG = 'TALB'
ID3_ALBUM_ARTIST_TAG = 'TPE2'
ID3_GENRE_TAG = 'TCON'
ID3_RATING_TAG = 'POPM'
ID3_RATING_APP_EMAIL = 'POPM:bodzify'
ID3_LANGUAGE_TAG = 'TLAN'

# FLAC files use Vorbis tags
VORBIS_TITLE_TAG = 'title'
VORBIS_ARTIST_TAG = 'artist'
VORBIS_ALBUM_TAG = 'album'
VORBIS_ALBUM_ARTISTS_TAG = 'albumartist'
VORBIS_GENRE_TAG = 'genre'
VORBIS_RATING_TAG = 'rating'
VORBIS_LANGUAGE_TAG = 'language'


def Update(oldTrack: LibraryTrack, newData: QueryDict, partial, TrackPutSerializerClass, user: User):
    mutableData = newData.copy()
    oldTrack = LibraryTrack.objects.get(uuid=oldTrack.uuid)
    oldGenre = oldTrack.genre
    oldArtist = oldTrack.artist
    oldAlbum = oldTrack.album

    if mutableData[LibraryTrackViewSet.DATA_GENRE_PARAMETER_NAME] is None:
        mutableData[LibraryTrackViewSet.DATA_GENRE_PARAMETER_NAME] = Criteria.objects.get(
                user=user, name=CriteriaSpecialNames.GENRE_GENRELESS).uuid

    artistName = mutableData[LibraryTrackViewSet.DATA_ARTIST_NAME_PARAMETER_NAME]    
    mutableData[LibraryTrackViewSet.DATA_ARTIST_PARAMETER_NAME] = (
            ArtistService.GetArtistFromNameAfterHavingEventuallyCreatedIt(user, artistName)).uuid

    albumName = mutableData[LibraryTrackViewSet.DATA_ALBUM_NAME_PARAMETER_NAME]  
    albumArtistsNamesString = mutableData[LibraryTrackViewSet.DATA_ALBUM_ARTISTS_NAMES_PARAMETER_NAME]  
    albumArtistsNamesList = GetArtistsNamesListFromString(albumArtistsNamesString)
    mutableData[LibraryTrackViewSet.DATA_ALBUM_PARAMETER_NAME] = (
            AlbumService.GetAlbumFromNameAndAlbumArtistsNamesAfterHavingEventuallyCreatedThem(
                    user=user, albumName=albumName, albumArtistsNames=albumArtistsNamesList)).uuid

    requestSerializer = TrackPutSerializerClass(oldTrack, data=mutableData, partial=partial)
    requestSerializer.is_valid(raise_exception=True)
    updatedTrack = requestSerializer.save()

    if oldGenre != updatedTrack.genre:
        PlaylistService.UpdatePlaylistsOfTrack(user=user, track=updatedTrack, oldGenre=oldGenre)

    if oldArtist != updatedTrack.artist and oldArtist != None:
        ArtistService.DeleteArtistIfNoTrackAndAlbumLinked(user=user, artist=oldArtist)

    if oldAlbum != updatedTrack.album and oldTrack != None:
        AlbumService.DeleteAlbumIfNoTrackLinked(user=user, album=oldAlbum)

    UpdateTags(updatedTrack)

    return updatedTrack


def UpdateTags(track: LibraryTrack):

    titleTag = track.title
    if titleTag is None:
        titleTag = ""    
    
    if track.artist_id is not None:
        artistTag = track.artist.name
    else:
        artistTag = ""     
    
    albumArtistsTag = ""
    if track.album_id is not None:
        albumTag = track.album.name

        albumArtistNamesIndex = 0
        for albumArtist in track.album.albumArtists.all():
            if albumArtistNamesIndex != 0:
                albumArtistsTag = albumArtistsTag + TAG_ARTISTS_SEPARATION_CHAR
            albumArtistsTag = albumArtistsTag + albumArtist.name
            albumArtistNamesIndex = albumArtistNamesIndex + 1
    else:
        albumTag = ""        
        
    if albumTag is None:
        albumTag = ""

    if track.genre is None:
        genreTag = ""
    else:
        genreTag = track.genre.name

    ratingTag = track.rating
    if ratingTag is None:
        ratingTag = 0

    languageTag = track.language
    if languageTag is None:
        languageTag = ""

    if track.fileExtension.lower() in [".wav", ".mp3"]:
        trackId3Tags = ID3(track.file.path)

        trackId3Tags.delall(ID3_TITLE_TAG)
        trackId3Tags.add(TIT2(encoding=3, text=titleTag))
        trackId3Tags.delall(ID3_ARTIST_TAG)
        trackId3Tags.add(TIT2(encoding=3, text=artistTag))
        trackId3Tags.delall(ID3_ALBUM_TAG)
        trackId3Tags.add(TIT2(encoding=3, text=albumTag))
        trackId3Tags.delall(ID3_ALBUM_ARTIST_TAG)
        trackId3Tags.add(TIT2(encoding=3, text=albumArtistsTag))
        trackId3Tags.delall(ID3_GENRE_TAG)
        trackId3Tags.add(TIT2(encoding=3, text=genreTag))
        trackId3Tags.delall(ID3_RATING_TAG)
        trackId3Tags.add(POPM(email=ID3_RATING_APP_EMAIL, rating=ratingTag))
        trackId3Tags.delall(ID3_LANGUAGE_TAG)
        trackId3Tags.add(TIT2(encoding=3, text=languageTag))

    elif track.fileExtension.lower() == ".flac":
        trackFlacTags = FLAC(track.file.path)
        trackFlacTags[VORBIS_TITLE_TAG] = titleTag
        trackFlacTags[VORBIS_ARTIST_TAG] = artistTag
        trackFlacTags[VORBIS_ALBUM_TAG] = albumTag
        trackFlacTags[VORBIS_ALBUM_ARTISTS_TAG] = albumArtistsTag
        trackFlacTags[VORBIS_GENRE_TAG] = genreTag
        trackFlacTags[VORBIS_RATING_TAG][0] = str(ratingTag)
        trackFlacTags[VORBIS_LANGUAGE_TAG] = languageTag
        trackFlacTags.save(track.file.path)


def GetValuesFirstElementIfExistInDicOrEmptyString(dic, key):
    if key in dic:
        return dic[key][0]
    else:
        return ""


def GetValuesFirstElementIfExistInDicOrZero(dic, key):
    if key in dic:
        return dic[key][0]
    else:
        return 0


def CreateFromUpload(user: User, uploadedFile):
    filename, fileExtension = os.path.splitext(uploadedFile.name)

    if fileExtension.lower() in [".wav", ".mp3"]:
        trackId3Tags = MutagenFile(uploadedFile)
        
        title = GetValuesFirstElementIfExistInDicOrEmptyString(trackId3Tags, ID3_TITLE_TAG)
        artistName = GetValuesFirstElementIfExistInDicOrEmptyString(trackId3Tags, ID3_ARTIST_TAG)
        albumName = GetValuesFirstElementIfExistInDicOrEmptyString(trackId3Tags, ID3_ALBUM_TAG)
        albumArtistsNamesString = (
                GetValuesFirstElementIfExistInDicOrEmptyString(trackId3Tags, ID3_ALBUM_ARTIST_TAG))

        if ID3_GENRE_TAG in trackId3Tags:
            genreName = trackId3Tags[ID3_GENRE_TAG][0]
        else:
            genreName = CriteriaSpecialNames.GENRE_GENRELESS

        duration = trackId3Tags.info.length 

        rating = 0
        for key in trackId3Tags.tags:
            if ID3_RATING_TAG in key:
                rating = trackId3Tags[key].rating

        language = GetValuesFirstElementIfExistInDicOrEmptyString(trackId3Tags, ID3_LANGUAGE_TAG)

    elif fileExtension.lower() == ".flac":
        trackFlacTags = FLAC(fileobj=uploadedFile)
        
        title = GetValuesFirstElementIfExistInDicOrEmptyString(trackFlacTags, VORBIS_TITLE_TAG)
        artistName = (
                GetValuesFirstElementIfExistInDicOrEmptyString(trackFlacTags, VORBIS_ARTIST_TAG))
        albumName = GetValuesFirstElementIfExistInDicOrEmptyString(trackFlacTags, VORBIS_ALBUM_TAG)
        albumArtistsNamesString = (
                GetValuesFirstElementIfExistInDicOrEmptyString(
                        trackFlacTags, VORBIS_ALBUM_ARTISTS_TAG))

        if VORBIS_GENRE_TAG in trackFlacTags:
            genreName = trackFlacTags[VORBIS_GENRE_TAG][0]
        else:
            genreName = CriteriaSpecialNames.GENRE_GENRELESS

        duration = trackFlacTags.info.length
        rating = GetValuesFirstElementIfExistInDicOrEmptyString(trackFlacTags, VORBIS_RATING_TAG)
        if rating == "":
            rating = "0"
        language = GetValuesFirstElementIfExistInDicOrEmptyString(
                trackFlacTags, VORBIS_LANGUAGE_TAG)

    genre = CriteriaService.GetCriteriaFromNameAfterHavingEventuallyCreatedIt(
            user=user, criteriaName=genreName)
    albumArtistsNamesList = GetArtistsNamesListFromString(albumArtistsNamesString)
    album = AlbumService.GetAlbumFromNameAndAlbumArtistsNamesAfterHavingEventuallyCreatedThem(
            user=user, albumName=albumName, albumArtistsNames=albumArtistsNamesList)
    artist = ArtistService.GetArtistFromNameAfterHavingEventuallyCreatedIt(
            user=user, artistName=artistName)
    track = LibraryTrack.objects.create(
            user=user,
            file=uploadedFile,
            title=title,
            artist=artist,
            album=album,
            genre=genre,
            duration=duration,
            rating=rating,
            language=language)
    AddTrackToGenrePlaylists(user, track)
    return track


def GetArtistsNamesListFromString(artistsNamesString: str) -> list:
    albumArtistsNamesWithEventualSpacesAround = (
            artistsNamesString.split(TAG_ARTISTS_SEPARATION_CHAR))
    return [it.strip() for it in  albumArtistsNamesWithEventualSpacesAround]


def AddTrackToGenrePlaylists(user: User, track: LibraryTrack):
    genre = track.genre
    while genre is not None:
        track.playlists.add(Playlist.objects.get(user=user, criteria=genre))
        genre = genre.parent
    track.save()


def CreateFromMineTrack(user: User, mineTrack: MineTrack, trackTempFileAbsolutePath: str):
    artist = ArtistService.GetArtistFromNameAfterHavingEventuallyCreatedIt(
        user=user, artistName=mineTrack.artist)
    
    # Tags of every myfreemp3 downloaded tracks are empty 
    libraryTrack = LibraryTrack(
        user=user, 
        title=mineTrack.title, 
        artist=artist, 
        album=None,
        genre=Criteria.objects.get(user=user, name=CriteriaSpecialNames.GENRE_GENRELESS),
        duration=mineTrack.duration,
        rating=0,
        language="")

    path = Path(trackTempFileAbsolutePath)
    with path.open(mode='rb') as f:
        libraryTrack.file = File(f, name=path.name)
        libraryTrack.save()
    

    libraryTrack.playlists.add(
            Playlist.objects.get(
                user=user, 
                name=PlaylistSpecialNames.GENRE_ALL))
    libraryTrack.playlists.add(
            Playlist.objects.get(
                user=user, 
                name=PlaylistSpecialNames.GENRE_GENRELESS))
    libraryTrack.save()

    UpdateTags(libraryTrack)

    return libraryTrack


def delete(uuid):
    track = LibraryTrack.objects.get(uuid=uuid)
    os.remove(track.path)
    track.delete()
