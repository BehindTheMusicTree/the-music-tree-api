from bodzify_api.model.musicbrainz_resource.Fields import Fields as MbResourceFields


class Fields(MbResourceFields):
    TITLE = 'title'
    SCORE = 'score'
    DURATION_IN_SEC = 'duration_in_sec'
    DURATION_STR_IN_HOUR_MIN_SEC = "duration_str_in_hour_min_sec"
    RELEASE_DATE = 'release_date'
    MUSICBRAINZ_ARTISTS = 'musicbrainz_artists'
    MUSICBRAINZ_LINK = 'musicbrainz_link'
