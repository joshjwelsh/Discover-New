import spotipy
import json
from collections import Counter
import random
import auth



count_page = ""
_description = "The playlists were made using an alogrithm specialized based on you. It works based on your liked songs playlist."

class Track:
    def __init__(self, uri, artists, name):
        self.uri = uri
        self.artists = artists
        self.name = name 
    
    def __str__(self):
        return f'Artist: {self.artists}, Name: {self.name}, Uri: {self.uri} \n'

    def __repr__(self):
        return f'Artist: {self.artists}, Name: {self.name}, Uri: {self.uri} \n'

# Return the playlist number
def getRecommendationCount():
    
    with open("temp.dat","r") as f:
        count_page = f.read()
    count = int(count_page)
    count += 1
    with open("temp.dat","w") as f:
        f.write(str(count))
    
    return str(count - 1)
        
    


def createPlaylist(sp, recom, idx):
    pl_name = f'Discover New { getRecommendationCount() }'   # Name for playlist

    playlist = sp.user_playlist_create(
        user=idx, name=pl_name, public=True, description=_description)
    playlistId = playlist['id']
    sp.playlist_add_items(playlist_id=playlistId, items=recom['uri'])


def recommendationEngine(sp, artist_dict):
    data = {x: v for (x,v) in artist_dict.items() if len(v) >= 1 and len(v) <= 5}
    artists = [v for v in data.keys()]
    # print(artists)
    recomm_tracks = list()
    for i in range(0,2):
        random.shuffle(artists)
        for idx, item in enumerate(artists):
            print(f"Idx - {idx} Item - {item}")
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
    # print(seeds)
    # print(len(seeds))
    #print(seeds[0])
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
    for count in range(10000):
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
                        #  = str(track['artists'][0]['name']) + " - " + str(track['name']) + "\n"
                        # #f.write(error_str)
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
    

    sp = auth.getLibrary()
    results = findList(sp)
    # scope = "user-library-modify"
    # sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret= client_secret, redirect_uri=redirect_url, scope=scope))
    # findDuplicates(sp, results)

    artistDict = createArtistDict(results)
    recom = recommendationEngine(sp, artistDict)
    me = sp.me()
    idx = me['id']

    sp = auth.setPlaylist()

    createPlaylist(sp, recom, idx)    
