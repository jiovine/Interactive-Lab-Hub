import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep
import qwiic_i2c
import qwiic_button
import board
from adafruit_seesaw import seesaw, rotaryio, digitalio
import qwiic_oled_display
import sys
import re


# sensors
seesaw = seesaw.Seesaw(board.I2C(), addr=0x36)
my_button1 = qwiic_button.QwiicButton()
my_button2 = qwiic_button.QwiicButton(0x5B)
seesaw.pin_mode(24, seesaw.INPUT_PULLUP)
button = digitalio.DigitalIO(seesaw, 24)
encoder = rotaryio.IncrementalEncoder(seesaw)
encoder.position = -50
pause = False
oled = qwiic_oled_display.QwiicOledDisplay()
oled.begin()
oled.clear(oled.PAGE)


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
oled.print("Now playing: {} by {}".format(track_id, artist))

while True:
    # next track and update display
    if my_button1.is_button_pressed():
        sp.next_track(device_id=DEVICE_ID)
        cur = sp.current_playback()
        track_id = cur['item']['name']
        track_id = re.sub(r'[^\x00-\x7f]', "", track_id)
        artist = cur['item']['artists'][0]['name']
        artist = re.sub(r'[^\x00-\x7f]', "", artist)
        print("{} by {}".format(track_id, artist))
        oled.clear(oled.PAGE)
        oled.begin()
        oled.clear(oled.PAGE)
        oled.print("Now playing: {} by {}".format(track_id, artist))

    # play/pause track
    if my_button2.is_button_pressed():
        if not pause:
            sp.pause_playback(device_id=DEVICE_ID)
            pause = not pause
        elif pause:
            sp.start_playback(device_id=DEVICE_ID)
            pause = not pause
    
    # volume knob, bounds it between 0 and 100
    position = -encoder.position
    if position >= 100:
        sp.volume(100, device_id=DEVICE_ID)
        encoder.position = -100
    elif position <= 0:
        sp.volume(0, device_id=DEVICE_ID)
        encoder.position = 0
    else:
        sp.volume(position, device_id=DEVICE_ID)
    oled.display()
    

    sleep(.05)

