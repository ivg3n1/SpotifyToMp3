import spotipy
import spotipy.util as util
from youtubesearchpython import VideosSearch
import sys
import os

def dir():#a function that returns the path to the script directory 
    os.chdir(sys.path[0]) #setting the cureent working directory to the directory of the script
    path = os.getcwd()
    os.makedirs(path , exist_ok = True)
    return(path) 

def spotify_to_list(token,playlist): #function that returns the whole spotify playlist as a list
    sp = spotipy.Spotify(auth=token)
    music_list = []
    off = 0
    while 1:
        if playlist == "Liked":
            results = sp.current_user_saved_tracks(limit = 20,offset=off * 20) #checks user's spotify song library
        else:
            results = sp.playlist_items(playlist_id=playlist, offset=off *20) #checks the playlist provided by the user
        for item in results['items']:
            track = item['track']
            if item == []:
                break
            music_list.append(track['name'] + ' - ' + track['artists'][0]['name']) #making a list of all the songs from the playlist
        off += 1
        if results['items'] == []:
                break
    return music_list

def download(path,music_list,sort): #this function downloads songs in mp3 format acoording to the spotify_to_list function
    with open("songs.txt","w") as f:
        pass
    place = 1
    if sort:  #deciding if music will be sorted by artist name
        song_path = path = os.path.join(path,"sorted")
    else:
        song_path = path = os.path.join(path,"mixed")    
    os.makedirs(path , exist_ok = True)
    print(music_list)
    for song in music_list:
        print(str(place) + '  ' +song)
        place += 1
        if sort:
            artist = song.split(' - ')
            song_path = os.path.join(path , artist[1])
            os.makedirs(song_path, exist_ok=True) #making a directory with the artists name
        if not(os.path.isfile(os.path.join(song_path,f"{song}.mp3"))): #checking if a song with that name already exists
            vs = VideosSearch(song+" lyrics") #searching fot the given song on youtube
            if not(vs.result()['result'] == []):
                vs = vs.result()["result"][0]["link"]#getting the link to the song from youtube
                os.system("youtube-dl -f bestaudio --extract-audio --audio-format mp3 -o {} {}".format(os.path.join(path , "NA.%%(ext)s"),vs)) #downloading the song from youtube
                try:
                    os.rename(os.path.join(path,"NA.mp3"),os.path.join(song_path,f"{song}.mp3")) #renames the downloaded file to the songs name
                    with open("songs.txt" , 'a') as f:
                        f.write(f"V {str(place)} {song}\n")
                except OSError:
                    try:
                        os.remove(os.path.join(path,"NA.mp3"))
                    except FileNotFoundError: 
                        with open("songs.txt" , 'a') as f:
                            f.write(f"X {place - 1} {song}\n")
        else:
            with open("songs.txt" , 'a') as f:
                f.write(f"V {str(place - 1)} {song}\n")

token = util.prompt_for_user_token(username = sys.argv[3], scope = 'user-library-read',client_id = sys.argv[4],client_secret = sys.argv[5], redirect_uri = 'https://localhost')

try:
    download(dir(),spotify_to_list(token,sys.argv[1]),False)
except spotipy.exceptions.SpotifyException:
    print("enter a valid url")
except UnicodeEncodeError:
    pass
