import json
import random
import spotipy
import cred as CRED
from collections import Counter
from spotipy.oauth2 import SpotifyOAuth

VERBOSE = False

class Config():
    def __init__(self,CRED):
        self.client_id = CRED.ID
        self.client_secret = CRED.SECRET
        self.redirect_url = CRED.REDIRECT
        self.scope = {
            "read-library": "user-library-read",
            "playlist-modify": "playlist-modify-public"
        }
    

count_page = ""
_description = "The playlists were made using an alogrithm specialized based on you. It works based on your liked songs playlist."


class App:


    def __init__(self):
        self.sp = None
        self.config = Config(CRED)
        if self.sp is None:
            self.createReadSp()
        

    def createReadSp(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=self.config.client_id, client_secret=self.config.client_secret, redirect_uri=self.config.redirect_url, scope=self.config.scopes["read-library"]))

    def createModifySp(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=self.config.client_id, client_secret=self.config.client_secret, redirect_uri=self.config.redirect_url, scope=self.config.scopes["playlist-modify"]))




class Track:
    def __init__(self, uri, artists, name):
        self.uri = uri
        self.artists = artists
        self.name = name 
    
    def __str__(self):
        return f'Artist: {self.artists}, Name: {self.name}, Uri: {self.uri} \n'

    def __repr__(self):
        return f'Artist: {self.artists}, Name: {self.name}, Uri: {self.uri} \n'



def getRecommendationCount():
    
    with open("temp.dat","r") as f:
        count_page = f.read()
    count = int(count_page)
    count += 1
    with open("temp.dat","w") as f:
        f.write(str(count))
    
    return str(count - 1)
        
    


def createPlaylist(sp, recom, idx):
    _name = f'Discover New { getRecommendationCount() }'   # Name for playlist

    playlist = sp.user_playlist_create(user=idx,name=_name, public=True,description=_description)
    playlistId = playlist['id']
    sp.playlist_add_items(playlist_id=playlistId, items=recom['uri'])

    


def recommendationEngine(sp, artist_dict):
    data = {x: v for (x,v) in artist_dict.items() if len(v) >= 1 and len(v) <= 5}
    if VERBOSE:
        print(f"data:\n\n{data}\n\n")
    artists = [v for v in data.keys()]
    if VERBOSE:
        print(f"artists:\n\n{artists}\n\n")
    recomm_tracks = list()
    for i in range(0,2):
        random.shuffle(artists)
        for idx, item in enumerate(artists):
            if idx == 5:
                break 
            track = data[item]
            recomm_tracks.append(track)

    random.shuffle(recomm_tracks)
    seeds = recomm_tracks[5:]
    print("Seeding........")
    for i , element in enumerate(seeds):
        print(i, ") ", element)
    uris = list()
    s = []

    for seed in seeds:
        if len(seed) >= 2:
            l = len(seed)
            r = random.randint(0, l-1)
            s.append(seed[r])

        else:
            s.append(seed)

    
    seeds = s
    if VERBOSE:
        print(f"Element s: {len(s)} {s}")




    if VERBOSE:
        print(f"Element seeds: {len(seeds)} {seeds}")


    for x in range(5):
        uris.append(seeds[x][0].uri)

    #trackData = [g.uri for g in uris]
    # print(uris)
    recommendations = sp.recommendations(seed_tracks=uris, limit=25)
    track = list()
    track_uri = list()
    for idx, item in enumerate(recommendations['tracks']):
        track.append(item['name'])
        track_uri.append(item['uri'])
        # print(track)

    return {
        'name': track,
        'uri': track_uri
    }
    
def createArtistDict(results):
    data = list()
    artist_dict = dict()

    for track in results:
        artist = str(track['artists'][0]['name'])
        uri = str(track['uri'])
        name = str(track['name'])
        item = Track(uri, artist, name)
        data.append(item)
    
    for item in data:
        if item.artists not in artist_dict:
            artist_dict[item.artists] = list()
            artist_dict[item.artists].append(item)

        else:
            artist_dict[item.artists].append(item)
    
    return artist_dict

def findList(sp):
    songs = list()
    for count in range(100):
        results = sp.current_user_saved_tracks(limit=20, offset=count*20 )
        if results is None:
            return songs
        else:
            for item in results['items']:
                if item is None:
                    return songs
                else:
                    with open('test1.txt', 'a') as f:
                        track = item['track']
                        songs.append(track)
                        error_str = str(track['artists'][0]['name']) + " - " + str(track['name']) + "\n"
                        #f.write(error_str)
    return songs
                    
def findDuplicates(sp ,results):
    duplicates = set()
    duplicates_data_index = list()
    error_str = list()
    error_data = list()

    for idx, track in enumerate(results):
        my_Str = str(track['artists'][0]['name']) + " - " + str(track['name']) + "\n"
        if my_Str not in duplicates:
            duplicates.add(my_Str)
            myIndex = str(idx) + '\n'
            duplicates_data_index.append(str(myIndex))
        else:
           error_str.append(my_Str)
           error_data.append(track['uri'])
        
    with open("duplicates_test_1_swartz.txt", 'w') as f:
        f.writelines(duplicates)
        f.close()
    with open("duplicates_test_2_swartz.txt", 'w') as f:
        f.writelines(duplicates_data_index)
        f.close()
    with open("errordata_test_3_swartz.txt", 'w') as f:
        f.writelines(error_str)
        f.close()    
    sp.current_user_saved_tracks_delete(tracks=error_data)


if __name__ == "__main__":


    config = Config(CRED)
    scope = "user-library-read"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config.client_id, client_secret=config.client_secret,
                                                   redirect_uri=config.redirect_url, scope=config.scope['read-library']))
    results = findList(sp)

    # scope = "user-library-modify"
    # sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret= client_secret, redirect_uri=redirect_url, scope=scope))
    # findDuplicates(sp, results)

    artistDict = createArtistDict(results)
    recom = recommendationEngine(sp, artistDict)
    me = sp.me()
    idx = me['id']

    scope = "playlist-modify-public"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config.client_id, client_secret=config.client_secret,
                                                   redirect_uri=config.redirect_url, scope=config.scope['playlist-modify']))
    createPlaylist(sp, recom, idx)    
