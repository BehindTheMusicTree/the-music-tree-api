from enum import Enum


class UploadedTrackTestFilename(str, Enum):
    """
    Enum for test audio filenames used in uploaded track tests.

    Each constant represents a test file with specific characteristics (metadata format,
    rating system, duration, etc.) used to validate audio file processing.
    """

    def __str__(self) -> str:
        return self.value

    # ============================================================================
    # DEFAULT
    # ============================================================================
    DEFAULT_MP3 = "default.mp3"

    # ============================================================================
    # ALBUM - Album metadata tests
    # ============================================================================
    ALBUM_KOKO_ID3V2_MP3 = "album=koko_id3v2.mp3"
    ALBUM_KOKO_ID3V2_WAV = "album=koko_id3v2.wav"
    ALBUM_KOKO_VORBIS_FLAC = "album=koko_vorbis.flac"
    ALBUM_ARTISTS_MUSE_ID3V2_MP3 = "album artists=muse_id3v2.mp3"
    ALBUM_ARTISTS_ONE_TWO_THREE_ANTISLASH_ID3V2 = "album artists=One Two Three_antislash_id3v2.mp3"
    ALBUM_ARTISTS_ONE_TWO_THREE_COMMA_ID3V2 = "album artists=One Two Three_comma_id3v2.mp3"
    ALBUM_ARTISTS_ONE_TWO_THREE_DOUBLE_ANTISLASH_ID3V2 = "album artists=One Two Three_double antislash_id3v2.mp3"
    ALBUM_ARTISTS_ONE_TWO_THREE_DOUBLE_SLASH_ID3V2 = "album artists=One Two Three_double slash_id3v2.mp3"
    ALBUM_ARTISTS_ONE_TWO_THREE_MULTI_TAGS_AND_SLASH_VORBIS = "album artists=One Two Three_muti tags and slash_vorbis.flac"
    ALBUM_ARTISTS_ONE_TWO_THREE_MULTI_TAGS_VORBIS = "album artists=One Two Three_muti tags_vorbis.flac"
    ALBUM_ARTISTS_ONE_TWO_THREE_SEMICOLON_ID3V2 = "album artists=One Two Three_semicolon_id3v2.mp3"
    ALBUM_ARTISTS_ONE_TWO_THREE_SLASH_ID3V2 = "album artists=One Two Three_slash_id3v2.mp3"

    # ============================================================================
    # ARTISTS - Artist metadata tests with various separator formats
    # ============================================================================
    ARTISTS_ONE_TWO_THREE_ANTISLASH_ID3V2_MP3 = "artists=One Two Three_antislash_id3v2.mp3"
    ARTISTS_ONE_TWO_THREE_ANTISLASH_ID3V2 = "artists=One Two Three_antislash_id3v2.mp3"
    ARTISTS_ONE_TWO_THREE_COMMA_ID3V2_MP3 = "artists=One Two Three_comma_id3v2.mp3"
    ARTISTS_ONE_TWO_THREE_COMMA_ID3V2 = "artists=One Two Three_comma_id3v2.mp3"
    ARTISTS_ONE_TWO_THREE_DOUBLE_ANTISLASH_ID3V2_MP3 = "artists=One Two Three_double antislash_id3v2.mp3"
    ARTISTS_ONE_TWO_THREE_DOUBLE_ANTISLASH_ID3V2 = "artists=One Two Three_double antislash_id3v2.mp3"
    ARTISTS_ONE_TWO_THREE_DOUBLE_SLASH_ID3V2_MP3 = "artists=One Two Three_double slash_id3v2.mp3"
    ARTISTS_ONE_TWO_THREE_DOUBLE_SLASH_ID3V2 = "artists=One Two Three_double slash_id3v2.mp3"
    ARTISTS_ONE_TWO_THREE_MULTI_TAGS_AND_SLASH_VORBIS = "artists=One Two Three_muti tags and slash_vorbis.flac"
    ARTISTS_ONE_TWO_THREE_MUTI_TAGS_AND_SLASH_VORBIS_FLAC = "artists=One Two Three_muti tags and slash_vorbis.flac"
    ARTISTS_ONE_TWO_THREE_MULTI_TAGS_VORBIS = "artists=One Two Three_muti tags_vorbis.flac"
    ARTISTS_ONE_TWO_THREE_MUTI_TAGS_VORBIS_FLAC = "artists=One Two Three_muti tags_vorbis.flac"
    ARTISTS_ONE_TWO_THREE_SEMICOLON_ID3V2_MP3 = "artists=One Two Three_semicolon_id3v2.mp3"
    ARTISTS_ONE_TWO_THREE_SEMICOLON_ID3V2 = "artists=One Two Three_semicolon_id3v2.mp3"
    ARTISTS_ONE_TWO_THREE_SLASH_ID3V2_MP3 = "artists=One Two Three_slash_id3v2.mp3"
    ARTISTS_ONE_TWO_THREE_SLASH_ID3V2 = "artists=One Two Three_slash_id3v2.mp3"

    # ============================================================================
    # BITRATE - Bitrate handling tests
    # ============================================================================
    BITRATE_1411_FLAC = "bitrate=1411.flac"
    BITRATE_IN_KBPS_BIG_1411_WAV = "bitrate in kbps_big=1411.wav"
    BITRATE_IN_KBPS_BIG_320_MP3 = "bitrate in kbps_big=320.mp3"
    BITRATE_IN_KBPS_BIG_946_FLAC = "bitrate in kbps_big=946.flac"
    BITRATE_IN_KBPS_SMALL_1152_WAV = "bitrate in kbps_small=1152.wav"
    BITRATE_IN_KBPS_SMALL_192_MP3 = "bitrate in kbps_small=192.mp3"
    BITRATE_IN_KBPS_SMALL_723_FLAC = "bitrate in kbps_small=723.flac"

    # ============================================================================
    # COPYRIGHT - Copyright metadata tests
    # ============================================================================
    COPYRIGHT_DOMAINE_PUBLIC_RIFF_WAV = "copyright=domaine public_riff.wav"

    # ============================================================================
    # DURATION - Duration handling and edge cases
    # ============================================================================
    DURATION_LESS_THAN_1_SEC_MP3 = "duration < 1 sec.mp3"
    DURATION_LESS_THAN_1_SEC_FLAC = "duration < 1 sec.flac"
    DURATION_LESS_THAN_1_SEC_WAV = "duration < 1 sec.wav"
    DURATION_1S_WAV = "duration=1s.wav"
    DURATION_1S_ISSUE_READING_FROM_MUTAGEN_AND_TYNITAG_WAV = "duration=1s issue reading from mutagen and tynitag.wav"
    DURATION_182_MP3 = "duration=182.mp3"
    DURATION_277S_MP3 = "duration=277s.mp3"
    DURATION_335S_FLAC = "duration=335s.flac"
    DURATION_472S_WAV = "duration=472s.wav"

    # ============================================================================
    # FILENAME - Filename format tests
    # ============================================================================
    FILENAME_WITH_SPACES_MP3 = "filename= with spaces .mp3"
    FILENAME_DODIDO_MYFREEMP3_VIP_MP3 = "filename=dodido myfreemp3.vip .mp3"
    FILENAME_DOT_IN_FILENAME_MP3 = "filename=dot.in.filename.mp3"
    FILENAME_DOTNOTINFILENAME_COPY_MP3 = "filename=dotnotinfilename copy.mp3"
    FILENAME_DOTNOTINFILENAME_MP3 = "filename=dotnotinfilename.mp3"

    # ============================================================================
    # FORMAT - File format validation and edge cases
    # ============================================================================
    FORMAT_BAD_WAV = "format=bad.wav"
    FORMAT_BAD_EXTENSION_MP4 = "format=bad_extension.mp4"
    FORMAT_CORRUPTED_WAV = "format=corrupted.wav"
    FORMAT_IMAGE_JPEG = "format=image.jpeg"
    FORMAT_IN_MEMORY_FLAC = "format=in_memory.flac"
    FORMAT_MD5_NOT_VALID_AND_CORRUPTED_FLAC = "format=md5 not valid and corrupted.flac"
    FORMAT_MD5_NOT_VALID_BECAUSE_OF_ID3V1_METADATA_FLAC = "format=md5 not valid because of id3v2 metadata.flac"
    FORMAT_MD5_NOT_VALID_NOT_BECAUSE_OF_ID3V1_METADATA_FLAC = "format=md5 not valid not because of id3v1 metadata.flac"

    # ============================================================================
    # GENRE - Genre metadata tests
    # ============================================================================
    GENRE_CODE_ID3V1_ABSTRACT_MP3 = "genre_code_id3v1=Abstract.mp3"
    GENRE_CODE_ID3V1_UNKNOWN_MP3 = "genre_code_id3v1=Unknown.mp3"

    # ============================================================================
    # METADATA - Metadata extraction with various tag formats and sizes
    # ============================================================================
    METADATA_NONE_MP3 = "metadata=none.mp3"
    METADATA_NONE_WAV = "metadata=none.wav"
    METADATA_NONE_FLAC = "metadata=none.flac"
    METADATA_LONG_A_ID3V1_SMALL_MP3 = "metadata=long a_id3v1_small.mp3"
    METADATA_LONG_A_ID3V1_SMALL_FLAC = "metadata=long a_id3v1_small.flac"
    METADATA_LONG_A_ID3V1_SMALL_WAV = "metadata=long a_id3v1_small.wav"
    METADATA_LONG_A_ID3V2_SMALL_MP3 = "metadata=long a_id3v2_small.mp3"
    METADATA_LONG_A_ID3V2_SMALL_FLAC = "metadata=long a_id3v2_small.flac"
    METADATA_LONG_A_ID3V2_SMALL_WAV = "metadata=long a_id3v2_small.wav"
    METADATA_LONG_A_VORBIS_SMALL_FLAC = "metadata=long a_vorbis_small.flac"
    METADATA_LONG_A_RIFF_SMALL_WAV = "metadata=long a_riff_small.wav"
    METADATA_LONG_A_ID3V1_BIG_FLAC = "metadata=long a_id3v1_big.flac"
    METADATA_LONG_A_ID3V1_BIG_MP3 = "metadata=long a_id3v1_big.mp3"
    METADATA_LONG_A_ID3V1_BIG_WAV = "metadata=long a_id3v1_big.wav"
    METADATA_LONG_A_ID3V2_BIG_FLAC = "metadata=long a_id3v2_big.flac"
    METADATA_LONG_A_ID3V2_BIG_MP3 = "metadata=long a_id3v2_big.mp3"
    METADATA_LONG_A_ID3V2_BIG_WAV = "metadata=long a_id3v2_big.wav"
    METADATA_LONG_A_RIFF_BIG_WAV = "metadata=long a_riff_big.wav"
    METADATA_LONG_A_VORBIS_BIG_FLAC = "metadata=long a_vorbis_big.flac"
    METADATA_WITH_ID3V23_WAV = "metadata=with id3v23.wav"

    # ============================================================================
    # OTHER - Special test files and edge cases
    # ============================================================================
    FINGERPRINT_MP3 = "fingerprint.mp3"
    FINGERPRINT_WAV = "fingerprint.wav"
    KWPD6ZD3Y5HQXBYFBNQ895XZYFF7YCVJJ0NF4VK5CFX5VT53FB8670J63MX2RUMGVZ46B78IQU6VQPJ7HYTZZLBBV5Q1L6TIP6MFZAFRNIDA8RREKPNCXBNRUKQTDZBUB7TW5ZN0MUKQX5GZGD5_MP3 = "kwPD6Zd3y5hQxbyFbNq895XZyFf7ycvJJ0Nf4vK5cFX5vt53fB8670j63Mx2ruMgVZ46B78iqu6vQpJ7hytZLbbv5Q1L6tiP6MfZAFRnidA8RrEKPnCxbNRUkQtdzBub7TW5zn0MuKqX5GzGd5.mp3"
    KWPD6ZD3Y5HQXBYFBNQ895XZYFF7YCVJJ0NF4VK5CFX5VT53FB8670J63MX2RUMGVZ46B78IQU6VQPJ7HYTZZLBBV5Q1L6TIP6MFZAFRNIDA8RREKPNCXBNRUKQTDZBUB7TW5ZN0MUKQX5GZGD51_MP3 = "kwPD6Zd3y5hQxbyFbNq895XZyFf7ycvJJ0Nf4vK5cFX5vt53fB8670j63Mx2ruMgVZ46B78iqu6vQpJ7hytZLbbv5Q1L6tiP6MfZAFRnidA8RrEKPnCxbNRUkQtdzBub7TW5zn0MuKqX5GzGd51.mp3"

    # ============================================================================
    # RATING - ID3v2 rating tests (MP3 files)
    # ============================================================================
    RATING_ID3V2_5_STAR_MP3 = "rating_id3v2=5 star.mp3"
    RATING_ID3V2_0_STAR_MP3 = "rating_id3v2=0 star.mp3"
    RATING_ID3V2_0_5_STAR_MP3 = "rating_id3v2=0.5 star.mp3"
    RATING_ID3V2_1_STAR_MP3 = "rating_id3v2=1 star.mp3"
    RATING_ID3V2_1_5_STAR_MP3 = "rating_id3v2=1.5 star.mp3"
    RATING_ID3V2_2_STAR_MP3 = "rating_id3v2=2 star.mp3"
    RATING_ID3V2_2_5_STAR_MP3 = "rating_id3v2=2.5 star.mp3"
    RATING_ID3V2_3_STAR_MP3 = "rating_id3v2=3 star.mp3"
    RATING_ID3V2_3_5_STAR_MP3 = "rating_id3v2=3.5 star.mp3"
    RATING_ID3V2_4_STAR_MP3 = "rating_id3v2=4 star.mp3"
    RATING_ID3V2_4_5_STAR_MP3 = "rating_id3v2=4.5 star.mp3"

    # ============================================================================
    # RATING - ID3v2 rating tests (FLAC files)
    # ============================================================================
    RATING_ID3V2_0_STAR_FLAC = "rating_id3v2=0 star.flac"
    RATING_ID3V2_0_5_STAR_FLAC = "rating_id3v2=0.5 star.flac"
    RATING_ID3V2_1_STAR_FLAC = "rating_id3v2=1 star.flac"
    RATING_ID3V2_1_5_STAR_FLAC = "rating_id3v2=1.5 star.flac"
    RATING_ID3V2_2_STAR_FLAC = "rating_id3v2=2 star.flac"
    RATING_ID3V2_2_5_STAR_FLAC = "rating_id3v2=2.5 star.flac"
    RATING_ID3V2_3_STAR_FLAC = "rating_id3v2=3 star.flac"
    RATING_ID3V2_3_5_STAR_FLAC = "rating_id3v2=3.5 star.flac"
    RATING_ID3V2_4_STAR_FLAC = "rating_id3v2=4 star.flac"
    RATING_ID3V2_4_5_STAR_FLAC = "rating_id3v2=4.5 star.flac"
    RATING_ID3V2_5_STAR_FLAC = "rating_id3v2=5 star.flac"
    RATING_ID3V2_NONE_WAV = "rating_id3v2=none.wav"

    # ============================================================================
    # RATING - ID3v2 Base 100 rating tests (WAV files)
    # ============================================================================
    RATING_ID3V2_BASE_100_0_STAR_WAV = "rating_id3v2_base 100=0 star.wav"
    RATING_ID3V2_BASE_100_0_5_STAR_WAV = "rating_id3v2_base 100=0.5 star.wav"
    RATING_ID3V2_BASE_100_1_STAR_WAV = "rating_id3v2_base 100=1 star.wav"
    RATING_ID3V2_BASE_100_1_5_STAR_WAV = "rating_id3v2_base 100=1.5 star.wav"
    RATING_ID3V2_BASE_100_2_STAR_WAV = "rating_id3v2_base 100=2 star.wav"
    RATING_ID3V2_BASE_100_2_5_STAR_WAV = "rating_id3v2_base 100=2.5 star.wav"
    RATING_ID3V2_BASE_100_3_STAR_WAV = "rating_id3v2_base 100=3 star.wav"
    RATING_ID3V2_BASE_100_3_5_STAR_WAV = "rating_id3v2_base 100=3.5 star.wav"
    RATING_ID3V2_BASE_100_4_STAR_WAV = "rating_id3v2_base 100=4 star.wav"
    RATING_ID3V2_BASE_100_4_5_STAR_WAV = "rating_id3v2_base 100=4.5 star.wav"
    RATING_ID3V2_BASE_100_5_STAR_WAV = "rating_id3v2_base 100=5 star.wav"

    # ============================================================================
    # RATING - ID3v2 Base 255 (KID3) rating tests (WAV files)
    # ============================================================================
    RATING_ID3V2_BASE_255_KID3_1_STAR_WAV = "rating_id3v2_base 255_kid3=1 star.wav"
    RATING_ID3V2_BASE_255_KID3_2_STAR_WAV = "rating_id3v2_base 255_kid3=2 star.wav"
    RATING_ID3V2_BASE_255_KID3_3_STAR_WAV = "rating_id3v2_base 255_kid3=3 star.wav"
    RATING_ID3V2_BASE_255_KID3_4_STAR_WAV = "rating_id3v2_base 255_kid3=4 star.wav"
    RATING_ID3V2_BASE_255_KID3_5_STAR_WAV = "rating_id3v2_base 255_kid3=5 star.wav"

    # ============================================================================
    # RATING - ID3v2 Traktor rating tests
    # ============================================================================
    RATING_ID3V2_TRACKTOR_1_STAR_MP3 = "rating_id3v2_tracktor=1 star.mp3"
    RATING_ID3V2_TRACKTOR_2_STAR_MP3 = "rating_id3v2_tracktor=2 star.mp3"
    RATING_ID3V2_TRACKTOR_3_STAR_MP3 = "rating_id3v2_tracktor=3 star.mp3"
    RATING_ID3V2_TRACKTOR_4_STAR_MP3 = "rating_id3v2_tracktor=4 star.mp3"
    RATING_ID3V2_TRACKTOR_5_STAR_MP3 = "rating_id3v2_tracktor=5 star.mp3"
    RATING_ID3V2_TRACKTOR_NONE_MP3 = "rating_id3v2_tracktor=none.mp3"

    # ============================================================================
    # RATING - Vorbis rating tests (FLAC files)
    # ============================================================================
    RATING_VORBIS_5_STAR_FLAC = "rating_vorbis=5 star.flac"
    RATING_VORBIS_0_STAR_FLAC = "rating_vorbis=0 star.flac"
    RATING_VORBIS_0_5_STAR_FLAC = "rating_vorbis=0.5 star.flac"
    RATING_VORBIS_1_STAR_FLAC = "rating_vorbis=1 star.flac"
    RATING_VORBIS_1_5_STAR_FLAC = "rating_vorbis=1.5 star.flac"
    RATING_VORBIS_2_STAR_FLAC = "rating_vorbis=2 star.flac"
    RATING_VORBIS_2_5_STAR_FLAC = "rating_vorbis=2.5 star.flac"
    RATING_VORBIS_3_STAR_FLAC = "rating_vorbis=3 star.flac"
    RATING_VORBIS_3_5_STAR_FLAC = "rating_vorbis=3.5 star.flac"
    RATING_VORBIS_4_STAR_FLAC = "rating_vorbis=4 star.flac"
    RATING_VORBIS_4_5_STAR_FLAC = "rating_vorbis=4.5 star.flac"
    RATING_VORBIS_TRAKTOR_1_STAR_FLAC = "rating_vorbis_traktor=1 star.flac"
    RATING_VORBIS_TRAKTOR_2_STAR_FLAC = "rating_vorbis_traktor=2 star.flac"
    RATING_VORBIS_TRAKTOR_3_STAR_FLAC = "rating_vorbis_traktor=3 star.flac"
    RATING_VORBIS_TRAKTOR_4_STAR_FLAC = "rating_vorbis_traktor=4 star.flac"
    RATING_VORBIS_TRAKTOR_5_STAR_FLAC = "rating_vorbis_traktor=5 star.flac"
    RATING_VORBIS_TRAKTOR_NONE_FLAC = "rating_vorbis_traktor=none.flac"

    # ============================================================================
    # RATING - RIFF/KID3 rating tests (WAV files)
    # ============================================================================
    RATING_RIFF_BASE_100_KID3_1_STAR_WAV = "rating_riff_base 100_kid3=1 star.wav"
    RATING_RIFF_BASE_100_KID3_2_STAR_WAV = "rating_riff_base 100_kid3=2 star.wav"
    RATING_RIFF_BASE_100_KID3_3_STAR_WAV = "rating_riff_base 100_kid3=3 star.wav"
    RATING_RIFF_BASE_100_KID3_4_STAR_WAV = "rating_riff_base 100_kid3=4 star.wav"
    RATING_RIFF_BASE_100_KID3_5_STAR_WAV = "rating_riff_base 100_kid3=5 star.wav"
    RATING_RIFF_KID3_NONE_WAV = "rating_riff_kid3=none.wav"

    # ============================================================================
    # RECORDING - MusicBrainz recording matching tests
    # ============================================================================
    RECORDING_ALLUMERLEFEU_2_MATCHES_ONE_WITH_MORE_RELEASE_GROUPS_MP3 = "recording=Allumerlefeu_2 matches one with more release groups.mp3"
    RECORDING_CALIFORNIA_GURLS_ID3V2_TAGS_FLAC = "recording=california gurls_id3v2 tags.flac"
    RECORDING_CELINEKIN_PARK_NO_MUSICBRAINZ_RECORDING_DURATION_MP3 = "recording=Celinekin Park - no musicbrainz recording duration.mp3"
    RECORDING_DANS_LA_LEGENDE_FLAC = "recording=Dans la legende.flac"
    RECORDING_JUAN_HANSEN_OOSTIL_DROWN_MASSANO_REMIX_7M21_MP3 = "recording=juan hansen oostil - drown (massano remix) - 7m21.mp3"
    RECORDING_JUAN_HANSEN_OOSTIL_DROWN_MASSANO_REMIX_7M20_FLAC = "recording=juan hansen oostil - drown (massano remix) - 7m20.flac"
    RECORDING_KEMAR_FRANCE_MP3 = "recording=Kemar - France.mp3"
    RECORDING_LORIE_2_MATCHES_BUT_ONE_WITH_CLOSEST_DURATION_MP3 = "recording=lorie_2_matches_but_one_with_closest_duration.mp3"
    RECORDING_QUEEN_25_MATCHES_BUT_ONE_WITH_BEST_DURATION_AND_MOST_FIELDS_AND_MOST_RELEASE_GROUPS_MP3 = "recording=queen_25_matches_but_one_with_best_duration_and_most_fields_and_most_release_groups.mp3"
    RECORDING_QUEEN_DURATION_181_MP3 = "recording=queen_duration_181.mp3"
    RECORDING_QUEEN_MULTIPLE_RELEASE_DATES_MP3 = "recording=queen_multiple_release_dates.mp3"
    RECORDING_QUEEN_WEARETHECHAMPIONS_MP3 = "recording=queen_wearethechampions.mp3"
    RECORDING_SHOWMUSTGOON_MP3 = "recording=showmustgoon.mp3"
    RECORDING_TOKYO_DRIFT_NO_MB_RECORDING_MP3 = "recording=Tokyo Drift_no mb recording.mp3"
    RECORDING_TOTAL_ECLIPSE_3_SCORES_FLAC = "recording=total eclipse_3 scores.flac"
    RECORDING_TOTAL_ECLIPSE_5M35_FLAC = "recording=total eclipse_5m35.flac"
    RECORDING_TOTAL_ECLIPSE_9_MATCHES_BUT_ONE_WITH_DURATION_FLAC = "recording=total eclipse_9 matches one with duration.flac"
    RECORDING_Y_DO_I_CARMINA_BURANA_REMIX_7M52_MP3 = "recording=Y do i - Carmina Burana Remix - 7m52.mp3"
    RECORDING_CARMINA_BURANA_REMIX_7M52_MP3 = "recording=Y do i - Carmina Burana Remix - 7m52.mp3"
    RECORDING_Y_DO_I_CARMINA_BURANA_REMIX_7M52_WAV = "recording=Y do i - Carmina Burana Remix - 7m52.wav"
    RECORDING_CARMINA_BURANA_REMIX_7M52_WAV = "recording=Y do i - Carmina Burana Remix - 7m52.wav"

    # ============================================================================
    # SIZE - File size handling tests
    # ============================================================================
    SIZE_BIG_26_6MO_FLAC = "size_big=26.6mo.flac"
    SIZE_BIG_79_55MO_WAV = "size_big=79.55mo.wav"
    SIZE_BIG_9_98MO_MP3 = "size_big=9.98mo.mp3"
    SIZE_SMALL_0_01MO_MP3 = "size_small=0.01mo.mp3"
    SIZE_SMALL_0_05MO_FLAC = "size_small=0.05mo.flac"
    SIZE_SMALL_0_08MO_WAV = "size_small=0.08mo.wav"
