from enum import Enum


class TestLibTrackFilename(str, Enum):
    ALBUM_ARTISTS_MUSE_ID3V2_MP3 = "album artists=muse_id3v2.mp3"
    ALBUM_KOKO_ID3V2_MP3 = "album=koko_id3v2.mp3"
    ALBUM_KOKO_ID3V2_WAV = "album=koko_id3v2.wav"
    ALBUM_KOKO_VORBIS_FLAC = "album=koko_vorbis.flac"
    COPYRIGHT_DOMAINE_PUBLIC_RIFF_WAV = "copyright=domaine public_riff.wav"
    DEFAULT_MP3 = "default.mp3"
    DURATION_LESS_THAN_1_SEC_MP3 = "duration < 1 sec.mp3"
    DURATION_177S_MP3 = "duration=177s.mp3"
    GENRE_ABSTRACT_ID3V1_MP3 = "genre=abstract_id3v1.mp3"
    RATING_1_STAR_ID3V2_MP3 = "rating=1 star_id3v2.mp3"
    RATING_1_STAR_ID3V2_WAV = "rating=1 star_id3v2.wav"
    RATING_1_STAR_VORBIS_FLAC = "rating=1 star_vorbis.flac"
    RECORDING_SHOWMUSTGOON_MP3 = "recording=showmustgoon.mp3"
    TAGS_ALL_ID3V2_FLAC = "tags=all_id3v2.flac"
    TAGS_MAX_A_ID32V2_WAV = "tags=max a_id32v2.wav"
    TAGS_MAX_A_MP3 = "tags=max a.mp3"
    TAGS_NONE_FLAC = "tags=none.flac"
    TAGS_NONE_MP3 = "tags=none.mp3"
    TAGS_NONE_WAV = "tags=none.wav"