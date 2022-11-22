import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep
import sys
import re


# spotify credentials
"""My credentials for spotify go here, for privacy reasons I removed them for github"""

# Spotify Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                client_secret=CLIENT_SECRET,
                                                redirect_uri="http://localhost:8080",
                                                scope="user-read-playback-state,user-modify-playback-state"))


# Transfer playback to the Raspberry Pi if music is playing on a different device
# or force start it on that device if there is no music playing
playlists = {'brett': 'spotify:playlist:6VChS0ZQoRSOWTNsP7TgLZ', 'feel good':'spotify:playlist:5xGQTmhIGvBeaPCVUtKTZB'}
sp.start_playback(device_id=DEVICE_ID, context_uri=playlists['brett'])
sp.shuffle(True, device_id=DEVICE_ID)
cur = sp.current_playback()
track_id = cur['item']['name']
track_id = re.sub(r'[^\x00-\x7f]', "", track_id)
artist = cur['item']['artists'][0]['name']
artist = re.sub(r'[^\x00-\x7f]', "", artist)
print("{} by {}".format(track_id, artist))