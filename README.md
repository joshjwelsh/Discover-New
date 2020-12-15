# Discover New 

Algorithmically create playlists based on spotify api and Spotipy wrapper. The point of the project is to create playlists based on the user's liked songs. 

The playlists are built using a randomized algorithm which preferentializes artists who you enjoy enough to add to your liked songs but you havent fully explored their discography. 

## Setup 

1. You must activate your Spotify developer [account](https://developer.spotify.com/)

2. Once activated, clone the repository and then create a file called cred.py . In the file add your ID, SECRET, and redirect URL (consider using localhost/9000).

3. Import the file to the recommendationEngine.py and simply modify this section with your cred.py file:
    
        client_id = cred.ID

        client_secret = cred.SECRET
        
        redirect_url = cred.REDIRECT

4. Run it using 

        >> python3 recommendationEngine.py 

5. Enjoy discovering new music 

## Important!

The temp.dat file is used to increment the name of the playlist. Simply reset temp.dat to 1 and then run the program. 


### This Project is still underdevelopment and you are welcome to fork and improve the design. 

