import os
import spotipy
from dotenv import load_dotenv
from urllib.parse import quote_plus
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
from itertools import chain
from datetime import date

load_dotenv()  # This loads the environment variables from .env

scope = "user-read-currently-playing,playlist-read-private,user-follow-read"

class Artist:
    def __init__(self, artist):
        self.id = artist["id"]
        self.name = artist["name"]
        self.popularity = artist["popularity"]
        self.followers = artist["followers"]["total"]
        self.genres = artist["genres"]
        self.image = artist["images"][0]["url"] if artist["images"] else None
        self.uri = artist["uri"]
        self.url = artist["external_urls"]["spotify"]
        self.albums = []
        self.tracks = []
        self.related = []

    def __repr__(self):
        return f'<Artist {self.name}>'

    def __str__(self):
        return f'{self.name}'
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)

class Track:
    def __init__(self, track):
        self.id = track["id"]
        self.name = track["name"]
        self.popularity = track["popularity"]
        self.duration_ms = track["duration_ms"]
        self.explicit = track["explicit"]
        self.artists = list(map(lambda a: a["name"], track["artists"]))
        self.album = track["album"]["name"]
        self.image = track["album"]["images"][0]["url"] if track["album"]["images"] else None
        self.uri = track["uri"]
        self.url = track["external_urls"]["spotify"]
        self.preview_url = track["preview_url"]
        self.is_local = track["is_local"]
#        self.is_playable = track["is_playable"]
        self.disc_number = track["disc_number"]
        self.track_number = track["track_number"]
        self.type = track["type"]
        self.explicit = track["explicit"]
        self.released_year = int(track["album"]["release_date"][:4])

    def __str__(self) -> str:
        return f'{self.name} by {self.artists}'

class Playlist:
    def __init__(self, playlist):
        self.id = playlist["id"]
        self.name = playlist["name"]
        self.description = playlist["description"]
        self.image = playlist["images"][0]["url"] if playlist["images"] else None
        self.uri = playlist["uri"]
        self.url = playlist["external_urls"]["spotify"]

# playing = sp.current_user_playing_track()
# print(playing["item"].keys())
# track_title = playing["item"]["name"]
# track_artists = list(map( lambda a: a["name"], playing["item"]["artists"]))
# print(f'You are listening to {track_title} by {track_artists}')

# related = sp.artist_related_artists(playing["item"]["artists"][0]["id"])
# other_artists = list(map(lambda a: a["name"], related["artists"]))
# print(other_artists)

def flatmap(func, *iterable):
    return chain.from_iterable(map(func, *iterable))

class SpotifyClient:
    def __init__(self, session = None, redirect_uri = 'http://localhost:9090'):
        cache_handler = FlaskSessionCacheHandler(session) if session else None
        self.auth_manager = SpotifyOAuth(scope=scope, cache_handler=cache_handler, redirect_uri=redirect_uri)
        self.sp = spotipy.Spotify(auth_manager=self.auth_manager, requests_timeout=20)

    def playlists(self):
        pls = self.sp.current_user_playlists()
        return list(map(lambda p: Playlist(p), pls["items"]))

    def playlist_songs(self,p):
        id = p.id if isinstance(p, Playlist) else p
        ss = self.sp.playlist(id)
        # convert each track to a Track object
        return list(map(lambda t: Track(t["track"]), ss["tracks"]["items"]))
    
    def playlist_artists(self,id):
        ss = self.playlist_songs(id)
        artists = flatmap(lambda s: s.artists, ss)
        return artists

    def search_artist(self,artist):
        """Look up an artist by name and return an artist object (dict)."""
        a = self.sp.search(q=f'artist="{artist}"',type='artist',limit=1)
        if a and a["artists"]:
            return Artist(a["artists"]["items"][0])

    def related_artists(self,artist):
        """Find related artists and return a list of artist objects.
        
        Accepts either an artist object (dict) with an 'id' item
        or a string containing the artist id
        """
        a = artist if isinstance(artist, str) else artist["id"]
        related = self.sp.artist_related_artists(a)
        return related["artists"]

    def following_artists(self):
        """Get a list of artists the current user follows."""
        return list(map(lambda a: Artist(a), self.sp.current_user_followed_artists(limit=50)["artists"]["items"]))

    def artist(self, artist_id):
        """Get an artist by id."""
        a = self.sp.artist(artist_id)
        return Artist(a)

    def is_authenticated(self):
        return self.sp.cache_handler.get_cached_token() != None

    def who_am_i(self):
        me = self.sp.current_user()
        return me["display_name"]