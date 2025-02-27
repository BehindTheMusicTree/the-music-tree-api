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

    FINGERPRINT_MP3 = "fingerprint.mp3"
    FINGERPRINT_WAV = "fingerprint.wav"

    FORMAT_BAD_EXTENSION_MP4 = "format=bad_extension.mp4"
    FORMAT_BAD_MP3 = "format=bad.mp3"
    FORMAT_IMAGE_JPEG = "format=image.jpeg"
    FORMAT_IN_MEMORY_FLAC = "format=in_memory.flac"
    FORMAT_MD5_NOT_VALID_AND_CORRUPTED_FLAC = "format=md5_not_valid_and_corrupted.flac"

    GENRE_ABSTRACT_ID3V1_MP3 = "genre=abstract_id3v1.mp3"

    RATING_1_STAR_ID3V2_MP3 = "rating=1 star_id3v2.mp3"
    RATING_1_STAR_ID3V2_WAV = "rating=1 star_id3v2.wav"
    RATING_1_STAR_VORBIS_FLAC = "rating=1 star_vorbis.flac"

    RECORDING_ALLUMERLEFEU_2_MATCHES_ONE_WITH_MORE_RELEASE_GROUPS_MP3 = \
        "recording=allumerlefeu_2_matches_one_with_more_release_groups.mp3"
    RECORDING_BONNIE_TYLER_TOTAL_ECLIPSE_OF_THE_HEART_5M35_FLAC_5M43_FLAC = \
        "recording=Bonnie Tyler - Total Eclipse of the Heart - 5m35.flac"
    RECORDING_CARMINAREMIX__472S_WAV = "recording=carminaremix 472s.wav"
    RECORDING_CELINEKIN_PARK_NO_MUSICBRAINZ_RECORDING_DURATION_MP3 = \
        "recording=Celinekin Park - no musicbrainz recording duration.mp3"
    RECORDING_JUAN_HANSEN_OOSTIL_DROWN_MASSANO_REMIX_7M20_FLAC = \
        "recording=juan hansen oostil - drown (massano remix) - 7m20.flac"
    RECORDING_JUAN_HANSEN_OOSTIL_DROWN_MASSANO_REMIX_7M21_MP3 = \
        "recording=juan hansen oostil - drown (massano remix) - 7m21.mp3"
    RECORDING_LORIE_2_MATCHES_BUT_ONE_WITH_CLOSEST_DURATION_MP3 = \
        "recording=lorie_2_matches_but_one_with_closest_duration.mp3"
    RECORDING_QUEEN_25_MATCHES_BUT_ONE_WITH_BEST_DURATION_AND_MOST_FIELDS_AND_MOST_RELEASE_GROUPS_MP3 = \
        "recording=queen_25_matches_but_one_with_best_duration_and_most_fields_and_most_release_groups.mp3"
    RECORDING_QUEEN_DURATION_181_MP3 = "recording=queen_duration_181.mp3"
    RECORDING_QUEEN_MULTIPLE_RELEASE_DATES_MP3 = "recording=queen_multiple_release_dates.mp3"
    RECORDING_QUEEN_WEARETHECHAMPIONS_MP3 = "recording=queen_wearethechampions.mp3"
    RECORDING_SHOWMUSTGOON_MP3 = "recording=showmustgoon.mp3"
    RECORDING_TEMPERATURE_NO_MUSICBRAINZ_RECORDING_MP3 = \
        "recording=Tokyo Drift x Temperature - no musicbrainz recording.mp3"
    RECORDING_TOTAL_ECLIPSE_3_SCORES_FLAC = "recording=total_eclipse_3_scores.flac"
    RECORDING_TOTAL_ECLIPSE_9_MATCHES_BUT_ONE_WITH_DURATION_FLAC = \
        "recording=total_eclipse_9_matches_but_one_with_duration.flac"
    RECORDING_CARMINA_BURANA_REMIX_7M52_MP3 = "recording=Y do i - Carmina Burana Remix - 7m52.mp3"
    RECORDING_CARMINA_BURANA_REMIX_7M52_WAV = "recording=Y do i - Carmina Burana Remix - 7m52.wav"

    TAGS_ALL_ID3V2_FLAC = "tags=all_id3v2.flac"
    TAGS_MAX_A_ID32V2_WAV = "tags=max a_id32v2.wav"
    TAGS_MAX_A_MP3 = "tags=max a.mp3"
    TAGS_NONE_FLAC = "tags=none.flac"
    TAGS_NONE_MP3 = "tags=none.mp3"
    TAGS_NONE_WAV = "tags=none.wav"
