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
from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist
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


def extract(user: User, extract_schema_data: QueryDict):
    mine_track_url_label = extract_schema_data[MINE_TRACK_ATTRIBUTES_LABEL.URL]
    track_in_memory_file = requests.get(mine_track_url_label, stream=True)
    with NamedTemporaryFile(delete=True) as track_temp_file:
        for block in track_in_memory_file.iter_content(1024 * 8):
            if not block:
                break
            track_temp_file.write(block)
        track_temp_file.flush()
        track_temp_file.seek(0)

        post_schema_data = _getSaveDataFromRequestData(extract_schema_data)

        track_filename, isFilenameRandomlyGenerated = _getTrackFilenameWithExtension(
            mine_track_url_label, extract_schema_data)
        post_schema_data[TRACK_ATTRIBUTES_LABEL.FILE] = File(
            track_temp_file, name=track_filename)
        library_track = create(user=user, post_schema_data=post_schema_data,
                              forceTitleGeneration=isFilenameRandomlyGenerated)

    return library_track


def create(user: User, post_schema_data: QueryDict, forceTitleGeneration: bool=False):
    serializer = TrackPostSchemaSerializer(data=post_schema_data)
    serializer.is_valid(raise_exception=True)

    file = post_schema_data[TRACK_ATTRIBUTES_LABEL.FILE]
    save_schema_data_from_file = _get_save_schema_data_from_file(file=file)
    save_schema_data = _get_dict1_overriden_with_dict2_when_key_is_provided(
        dict1=save_schema_data_from_file, dict2=post_schema_data)
    save_schema_data[TRACK_ATTRIBUTES_LABEL.USER] = user.id

    if TRACK_ATTRIBUTES_LABEL.TITLE not in save_schema_data:
        filename = os.path.basename(file.name).split('.')[0]
        if len(filename) > settings.TRACK_FILENAME_MAX_CHAR or forceTitleGeneration:
            title = settings.TRACK_GENERATED_TITLE_PREFIXE + \
                _generateShortUu(settings.TRACK_GENERATED_TITLE_LEN -
                                 len(settings.TRACK_GENERATED_TITLE_PREFIXE))
        else:
            title = filename
        save_schema_data[TRACK_ATTRIBUTES_LABEL.TITLE] = title

    return _save(user=user, save_schema_data=save_schema_data)


def update(user: User, update_schema_data: QueryDict, oldTrack: LibraryTrack):
    serializer = TrackUpdateSchemaSerializer(data=update_schema_data)
    serializer.is_valid(raise_exception=True)
    return _save(user=user, save_schema_data=update_schema_data, old_track=oldTrack)


def _save(user: User, save_schema_data: QueryDict, old_track: LibraryTrack = None):
    save_model_data = _get_save_model_data_from_save_schema_data(user=user, save_schema_data=save_schema_data)
    save_model_data[TRACK_ATTRIBUTES_LABEL.USER] = user.id
    save_serializer = TrackSaveModelSerializer(instance=old_track, data=save_model_data, partial=True)
    save_serializer.is_valid(raise_exception=True)
    saved_track = save_serializer.save()

    _add_track_to_genres_playlists(saved_track)
    _update_file_tags_if_file_exists(saved_track)

    return saved_track


def _get_save_schema_data_from_file(file):
    metadataDict = AudioMetadataService.get_metadata_dict_from_file(
        file=file, normalized_rating_max_value=settings.TRACK_RATING_MAX_VALUE)

    saveData = _removeNoneOrEmptyKeyFromDict(metadataDict)
    saveData[TRACK_ATTRIBUTES_LABEL.FILE] = file

    return saveData


def _removeNoneOrEmptyKeyFromDict(dict):
    for key in list(dict.keys()):
        if dict[key] is None or dict[key] == "":
            del dict[key]
    return dict


def _get_dict1_updated_with_artist_uuid_if_artist_name_in_dict2(
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


def _get_dict1_updated_with_album_uuid_if_album_name_in_dict2(
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


def _get_dict1_updated_with_genre_uuid_if_genre_name_in_dict2(
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


def _update_file_tags_if_file_exists(track: LibraryTrack):
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

    AudioMetadataService.update(
        file=track.file,
        metadata_update_dict=metadataUpdateDict,
        normalized_rating_max_value=settings.TRACK_RATING_MAX_VALUE)


def _getArtistsNameListFromString(namesString: str) -> list:
    namesWithEventualSpacesAroundAndDuplicates = namesString.split(
        AudioMetadataService.TAG_ARTISTS_SEPARATION_CHAR)
    names = list()
    for nameWithEventualSpacesAround in namesWithEventualSpacesAroundAndDuplicates:
        name = nameWithEventualSpacesAround.strip()
        if name != "" and names.count(name) == 0:
            names.append(name)
    return names


def _add_track_to_genres_playlists(track: LibraryTrack):
    genre = track.genre
    while genre is not None:
        track.playlists.add(CriteriaPlaylist.objects.get(
            user=track.user, type_id=CriteriaTypesId.GENRE, criteria=genre))
        genre = genre.parent
    track.save()


def _get_dict1_overriden_with_dict2_when_key_is_provided(dict1: QueryDict, dict2: QueryDict) -> dict:
    overridenDict1 = dict1.copy()
    for key in [TRACK_ATTRIBUTES_LABEL.FILE,
                TRACK_ATTRIBUTES_LABEL.TITLE,
                TRACK_SCHEMA_ATTRIBUTES_LABEL.ARTIST_NAME,
                TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME,
                TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAME_STRING,
                TRACK_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME,
                TRACK_ATTRIBUTES_LABEL.RATING,
                TRACK_ATTRIBUTES_LABEL.LANGUAGE]:
        overridenDict1 = _get_dict1_updated_with_dict2_key_if_set(
            key=key,
            dict1=overridenDict1,
            dict2=dict2)
    return overridenDict1

def _get_save_model_data_from_save_schema_data(user: User, save_schema_data: QueryDict) -> dict:
    save_model_data = dict()

    save_model_data = _get_dict1_updated_with_dict2_key_if_set(
        key=TRACK_ATTRIBUTES_LABEL.FILE,
        dict1=save_model_data,
        dict2=save_schema_data)

    save_model_data = _get_dict1_updated_with_dict2_key_if_set(
        key=TRACK_ATTRIBUTES_LABEL.TITLE,
        dict1=save_model_data,
        dict2=save_schema_data)

    save_model_data = _get_dict1_updated_with_artist_uuid_if_artist_name_in_dict2(
        user=user, dict1=save_model_data, dict2=save_schema_data)

    save_model_data = _get_dict1_updated_with_album_uuid_if_album_name_in_dict2(
        user=user, dict1=save_model_data, dict2=save_schema_data)

    save_model_data = _get_dict1_updated_with_genre_uuid_if_genre_name_in_dict2(
        user=user, dict1=save_model_data, dict2=save_schema_data)

    save_model_data = _get_dict1_updated_with_dict2_key_if_set(
        key=TRACK_ATTRIBUTES_LABEL.DURATION,
        dict1=save_model_data,
        dict2=save_schema_data)

    save_model_data = _get_dict1_updated_with_dict2_key_if_set(
        key=TRACK_ATTRIBUTES_LABEL.RATING,
        dict1=save_model_data,
        dict2=save_schema_data)

    save_model_data = _get_dict1_updated_with_dict2_key_if_set(
        key=TRACK_ATTRIBUTES_LABEL.LANGUAGE,
        dict1=save_model_data,
        dict2=save_schema_data)

    return save_model_data

def _get_dict1_updated_with_dict2_key_if_set(
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
