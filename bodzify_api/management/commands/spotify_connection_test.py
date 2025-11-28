import logging

from django.core.management.base import BaseCommand, CommandError

from bodzify_api.exception import spotify as spotify_exception
from bodzify_api.utils.spotify_api.SpotifyClient import SpotifyClient


logger = logging.getLogger('bodzify_api')


class Command(BaseCommand):
    help = 'Test the connection to Spotify API'

    def add_arguments(self, parser):
        parser.add_argument('--search', type=str, help='Optional search query to test')
        parser.add_argument('--artist', type=str, help='Optional artist ID to test')
        parser.add_argument('--track', type=str, help='Optional track ID to test')
        parser.add_argument('--isrc', type=str, help='Optional ISRC code to test')

    def handle(self, *args, **options):
        try:
            self.stdout.write(self.style.SUCCESS('Creating Spotify API service...'))
            service = SpotifyClient()
            self.stdout.write(self.style.SUCCESS('Successfully authenticated with Spotify API!'))

            # Test search functionality if search query provided
            search_query = options.get('search')
            if search_query:
                self.stdout.write(f'Searching for tracks with query: {search_query}')
                results = service.search_track(search_query, limit=5)
                tracks = results.get('tracks', {}).get('items', [])
                self.stdout.write(self.style.SUCCESS(f'Found {len(tracks)} tracks'))

                for i, track in enumerate(tracks[:5], 1):
                    self.stdout.write(
                        f"{i}. {track.get('name')} by {', '.join([a.get('name') for a in track.get('artists', [])])}")

            # Test get track by ID if track ID provided
            track_id = options.get('track')
            if track_id:
                self.stdout.write(f'Getting track with ID: {track_id}')
                track = service.retrieve_track_by_id(track_id)
                self.stdout.write(self.style.SUCCESS(
                    f"Track: {track.get('name')} by {', '.join([a.get('name') for a in track.get('artists', [])])}"
                ))

                # Test audio features
                self.stdout.write(f'Getting audio features for track: {track_id}')
                features = service.get_audio_features(track_id)
                self.stdout.write(self.style.SUCCESS(
                    f"Audio features: Tempo: {features.get('tempo')}, Key: {features.get('key')}, "
                    f"Energy: {features.get('energy')}, Danceability: {features.get('danceability')}"
                ))

            # Test get artist by ID if artist ID provided
            artist_id = options.get('artist')
            if artist_id:
                self.stdout.write(f'Getting artist with ID: {artist_id}')
                artist = service.get_artist_by_id(artist_id)
                self.stdout.write(self.style.SUCCESS(
                    f"Artist: {artist.get('name')}, Genres: {', '.join(artist.get('genres', []))}, "
                    f"Popularity: {artist.get('popularity')}"
                ))

            # Test get track by ISRC if ISRC code provided
            isrc = options.get('isrc')
            if isrc:
                self.stdout.write(f'Looking up track with ISRC: {isrc}')
                track = service.retrieve_track_by_isrc(isrc)
                if track:
                    self.stdout.write(self.style.SUCCESS(
                        f"ISRC match found: {track.get('name')} by {', '.join([a.get('name') for a in track.get('artists', [])])}"
                    ))
                else:
                    self.stdout.write(self.style.WARNING(f'No track found with ISRC: {isrc}'))

            if not any([search_query, track_id, artist_id, isrc]):
                self.stdout.write(self.style.SUCCESS(
                    'Connection to Spotify API verified! Use --search, --track, --artist, or --isrc to test specific functionality.'
                ))

        except spotify_exception.SpotifyAuthenticationException as e:
            raise CommandError(f'Authentication with Spotify failed: {str(e)}')
        except spotify_exception.SpotifyException as e:
            raise CommandError(f'Spotify API error: {str(e)}')
        except Exception as e:
            raise CommandError(f'Unexpected error: {str(e)}')
