import spotipy
import credentials
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, jsonify

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
            result = "Playing: Nothing"
        
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
    
class SpotifyAPI():
    def __init__(self):
        self.app = Flask(__name__)
        self.auth_manager, self.spotify = self.create_spotify(credentials.scope, credentials.username, credentials.client_id, credentials.client_secret)

        self.allowed_ips = ["178.203.204.190", "3.65.42.173"]

        self.app.route('/current_song')(self.get_current_song)
        self.app.route('/recently_played')(self.get_recently_played)
        self.app.route('/top_tracks')(self.get_top_tracks)
        self.app.route('/top_artists')(self.get_top_artists)

    def create_spotify(self, SCOPE, USERNAME, CLIENT_ID, CLIENT_SECRET):
        AUTH_MANAGER = SpotifyOAuth(
            scope=SCOPE,
            username=USERNAME,
            redirect_uri='http://127.0.0.1:5500/',
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            show_dialog=False)

        spotify = spotipy.Spotify(auth_manager=AUTH_MANAGER)

        return AUTH_MANAGER, spotify

    def check_ip_whitelist(self, ip):
        return ip in self.allowed_ips

    def validate_ip(self):
        client_ip = request.remote_addr
        if not self.check_ip_whitelist(client_ip):
            return jsonify({"error": "Access denied. Your IP is not whitelisted."}), 403

    def get_current_song(self):
        return self.validate_ip() or jsonify(self.pretty_print_current_song(self.spotify))
    
    def get_recently_played(self):
        return self.validate_ip() or jsonify(self.pretty_print_recently_played(self.spotify))
    
    def get_top_tracks(self):
        return self.validate_ip() or jsonify(self.pretty_print_top_tracks(self.spotify))
    
    def get_top_artists(self):
        return self.validate_ip() or jsonify(self.pretty_print_top_artists(self.spotify))

    def run(self):
        self.app.run(host='0.0.0.0', port=5000)  # Change host to '127.0.0.1' to only allow localhost access



def main():
    #auth_manager, spotify = Spotify.create_spotify(credentials.scope, credentials.username, credentials.client_id, credentials.client_secret)
    spotify_api = SpotifyAPI()
    spotify_api.run()

    #print(Spotify.pretty_print_current_song(spotify)[0])
    #print(Spotify.pretty_print_recently_played(spotify))
    #print(Spotify.pretty_print_top_tracks(spotify))
    #print(Spotify.pretty_print_top_artists(spotify))

if __name__ == "__main__":
    main()