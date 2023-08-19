import spotipy
import credentials
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, abort
from flask_cors import CORS, cross_origin # Import CORS from flask_cors
import logging

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

api_keys = credentials.api_keys  # Replace with your API keys

app = Flask(__name__)
CORS(app)

class Spotify():
    def create_spotify(SCOPE, USERNAME, CLIENT_ID, CLIENT_SECRET):
        AUTH_MANAGER = SpotifyOAuth(
        scope=SCOPE,
        username=USERNAME,
        redirect_uri='http://127.0.0.1:5500/',
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=False)
    
        spotify = spotipy.Spotify(auth_manager=AUTH_MANAGER)

        return AUTH_MANAGER, spotify

    def pretty_print_current_song(spotify):
        playing = spotify.currently_playing()
        
        if playing:
            song_info = spotify.current_user_playing_track()
            song_name = song_info["item"]["name"]
            artist_name = song_info["item"]["artists"][0]["name"]
            song_link = song_info["item"]["external_urls"]["spotify"]
            
            result = [
                f"Playing: {song_name} by {artist_name}",
                song_link
            ]
        else:
            result = ["Playing: Nothing", 0]
        
        return result

        
    def pretty_print_recently_played(spotify):
        played = spotify.current_user_recently_played(limit=10)
        song_list = []

        for item in played['items']:
            track = item['track']
            artists = ', '.join([artist['name'] for artist in track['artists']])
            song_name = track['name']
            song_link = track['external_urls']['spotify']
            
            song_info = f"{song_name} by {artists}", song_link
            song_list.append(song_info)
        
        return song_list

    def pretty_print_top_tracks(spotify):
        top_tracks = spotify.current_user_top_tracks(limit=10)

        formatted_tracks = []
        for track in top_tracks['items']:
            artists = ", ".join([artist['name'] for artist in track['artists']])
            track_name = track['name']
            track_url = track['external_urls']['spotify']

            formatted_track = f"{track_name} by {artists}, {track_url}"
            formatted_tracks.append(formatted_track)

        return formatted_tracks
    
    def pretty_print_top_artists(spotify):
        top_artists = spotify.current_user_top_artists(limit=10)
    
        formatted_artists = []
        for artist in top_artists['items']:
            artist_name = artist['name']
            artist_url = artist['external_urls']['spotify']

            formatted_artist = f"{artist_name}, {artist_url}"
            formatted_artists.append(formatted_artist)

        return formatted_artists

def main():
    auth_manager, spotify = Spotify.create_spotify(credentials.scope, credentials.username, credentials.client_id, credentials.client_secret)
    
    #print(spotify.currently_playing())
    #print(Spotify.pretty_print_current_song(spotify)[0])
    #print(Spotify.pretty_print_recently_played(spotify))
    #print(Spotify.pretty_print_top_tracks(spotify))
    #print(Spotify.pretty_print_top_artists(spotify))

app = Flask(__name__)

@app.route("/api/current-song")
def current_song():
    client_api_key = request.args.get("api_key")
    if client_api_key not in api_keys:
        abort(403)  # Forbidden status code

    client_ip = request.remote_addr
    logging.info(f"Visited by IP: {client_ip}")

    auth_manager, spotify = Spotify.create_spotify(credentials.scope, credentials.username, credentials.client_id, credentials.client_secret)
    
    song_info = Spotify.pretty_print_current_song(spotify)[0]
    
    return {
        "song": song_info
    }

@app.route("/api/recently-played")
def recently_played():
    client_api_key = request.args.get("api_key")
    if client_api_key not in api_keys:
        abort(403)  # Forbidden status code

    auth_manager, spotify = Spotify.create_spotify(credentials.scope, credentials.username, credentials.client_id, credentials.client_secret)
    
    played = Spotify.pretty_print_recently_played(spotify)
    
    return {
        "songs": played
    }

@app.route("/api/top-tracks")
def top_tracks():
    client_api_key = request.args.get("api_key")
    if client_api_key not in api_keys:
        abort(403)  # Forbidden status code

    auth_manager, spotify = Spotify.create_spotify(credentials.scope, credentials.username, credentials.client_id, credentials.client_secret)
    
    top_tracks = Spotify.pretty_print_top_tracks(spotify)
    
    return {
        "tracks": top_tracks
    }

@app.route("/api/top-artists")
def top_artists():
    client_api_key = request.args.get("api_key")
    if client_api_key not in api_keys:
        abort(403)  # Forbidden status code

    auth_manager, spotify = Spotify.create_spotify(credentials.scope, credentials.username, credentials.client_id, credentials.client_secret)
    
    top_artists = Spotify.pretty_print_top_artists(spotify)
    
    return {
        "artists": top_artists
    }

if __name__ == "__main__":
    #main()
    app.run(debug=True, port=8000)

