from msilib.schema import Error


def createPlaylist(sp, recom, idx):
    # Name for playlist
    pl_name = f'Discover New { getRecommendationCount() }'
    _description = "The playlists were made using an alogrithm specialized based on you. It works based on your liked songs playlist."

    playlist = sp.user_playlist_create(
        user=idx, name=pl_name, public=True, description=_description)
    playlistId = playlist['id']
    sp.playlist_add_items(playlist_id=playlistId, items=recom['uri'])
# Return the playlist number


def getRecommendationCount():

    with open("temp.dat", "r") as f:
        count_page = f.read()
    count = int(count_page)
    count += 1
    with open("temp.dat", "w") as f:
        f.write(str(count))

    return str(count - 1)


def findList(sp):
	songs = list()
	for count in range(10000):
		results = sp.current_user_saved_tracks(limit=20, offset=count*20)
	
		if results is None:
			if songs is None:
				print("Error: empty songs list")
				exit(1)
			else:
				return songs
		else:
			for item in results['items']:
				if item is None:
					return songs
				else:
					track = item['track']
					songs.append(track)
					
	return songs
