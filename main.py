import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred_swartz
scope = "user-read-recently-played"

client_id = cred_swartz.ID
client_secret = cred_swartz.SECRET
redirect_url = cred_swartz.REDIRECT

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret= client_secret, redirect_uri=redirect_url, scope=scope))

results = sp.current_user_recently_played()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])