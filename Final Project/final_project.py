from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep
import re
import album_list
from adafruit_servokit import ServoKit

# Set channels to the number of servo channels on your kit
kit = ServoKit(channels=16)

# Name and set up the servo to channel 0
servo = kit.continuous_servo[0]
# set pulse with range of servo
servo.set_pulse_width_range(10, 0)

# spotify credentials
"""My credentials for spotify go here, for privacy reasons I removed them for github"""



# Spotify Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                client_secret=CLIENT_SECRET,
                                                redirect_uri="http://localhost:8080",
                                                scope="user-read-playback-state,user-modify-playback-state"))

# create reader
reader=SimpleMFRC522()
# make sure the album isn't on shuffle to mimic a record player
sp.shuffle(False, device_id=DEVICE_ID)
# start the turn-table
servo.throttle = 0
        
# infinite loop waiting for RFID scan
while True:
    try:
        # Get tag ID from RFID scanner and convert to Spotify URI
        id= reader.read()[0]
        status = album_list.get_album(id)
        sleep(.5)
        # Checks if a song is currently playing
        # if it is and is the same album as what is scanned we do nothing
        # if it is a new album we start playing the new one
        cur_album_uri = sp.current_playback()['item']['album']['uri']
        is_playing = sp.current_playback()['is_playing']
        if is_playing and cur_album_uri == status:
            pass
        elif status and cur_album_uri != status:
            sleep(.1)
            sp.start_playback(device_id=DEVICE_ID, context_uri=status)
            sleep(.5)
            cur = sp.current_playback()
            artist = cur['item']['artists'][0]['name']
            artist = re.sub(r'[^\x00-\x7f]', "", artist)
            album = cur['item']['album']['name']
            print('Now playing: ' + album + ' by ' + artist) 
            sleep(.5)
        # if the tag scanned does not have an album linked to it
        else:
            sleep(0.25)
            print('No album on this tag: ' + str(id))
    
    # Stop the motor and playback when interrupting the script
    except KeyboardInterrupt:
        sp.pause_playback(device_id=DEVICE_ID)
        servo.throttle = 1
        sleep(0.5)
        break
