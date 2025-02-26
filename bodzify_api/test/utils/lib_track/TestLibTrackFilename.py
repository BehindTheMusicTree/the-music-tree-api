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
    DURATION_1_SEC_ISSUE_READING_FROM_MUTAGEN_AND_TYNITAG_WAV = \
        "duration=1_sec_issue_reading_from_mutagen_and_tynitag.wav"
    DURATION_472S_WAV = "duration=472s.wav"
    GENRE_ABSTRACT_ID3V1_MP3 = "genre=abstract_id3v1.mp3"
    RATING_1_STAR_ID3V2_MP3 = "rating=1 star_id3v2.mp3"
    RATING_1_STAR_ID3V2_WAV = "rating=1 star_id3v2.wav"
    RATING_1_STAR_VORBIS_FLAC = "rating=1 star_vorbis.flac"
    RECORDING_ALLUMERLEFEU_2_MATCHES_ONE_WITH_MORE_RELEASE_GROUPS_MP3 = \
        "recording=allumerlefeu_2_matches_one_with_more_release_groups.mp3"
    RECORDING_CARMINAREMIX__472S_WAV = "recording=carminaremix 472s.wav"
    RECORDING_JUAN_HANSEN_OOSTIL_DROWN_MASSANO_REMIX_7M20_FLAC = \
        "recording=juan hansen oostil - drown (massano remix) - 7m20.flac"
    RECORDING_SHOWMUSTGOON_MP3 = "recording=showmustgoon.mp3"
    RECORDING_CARMINA_BURANA_REMIX_7M52_MP3 = "recording=Y do i - Carmina Burana Remix - 7m52.mp3"
    RECORDING_CARMINA_BURANA_REMIX_7M53_WAV = "recording_Y do i - Carmina Burana Remix - 7m53.wav"
    TAGS_ALL_ID3V2_FLAC = "tags=all_id3v2.flac"
    TAGS_MAX_A_ID32V2_WAV = "tags=max a_id32v2.wav"
    TAGS_MAX_A_MP3 = "tags=max a.mp3"
    TAGS_NONE_FLAC = "tags=none.flac"
    TAGS_NONE_MP3 = "tags=none.mp3"
    TAGS_NONE_WAV = "tags=none.wav"
