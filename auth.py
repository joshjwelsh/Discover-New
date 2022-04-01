import cred
from spotipy.oauth2 import SpotifyOAuth
import spotipy


client_id = cred.ID
client_secret = cred.SECRET
redirect_url = cred.REDIRECT
scope = cred.USER_LIBRARY_READ
scope = cred.PLAYLIST_MODIFY_PUBLIC

def getLibrary():
	sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id, client_secret=client_secret, redirect_uri=redirect_url, scope=scope))   
	return sp

def setPlaylist():
	sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret, redirect_uri=redirect_url, scope=scope))
	return sp