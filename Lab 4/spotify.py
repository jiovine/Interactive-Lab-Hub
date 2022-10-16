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
devices = {'iphone':'fb28f830b5a710a6b6c42fc090b0deaf671ad287', 'macbook':'b02fe9efab907100102cb3f9c9cce0c723e6e4c0'}
DEVICE_ID=devices['macbook']
CLIENT_ID="52487af046974ab39977ea825c1baa2a"
CLIENT_SECRET="710facf1ad434d4da63f09822bdf17b4"

# Spotify Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                client_secret=CLIENT_SECRET,
                                                redirect_uri="http://localhost:8080",
                                                scope="user-read-playback-state,user-modify-playback-state"))


# Transfer playback to the Raspberry Pi if music is playing on a different device
# or force start it on that device if there is no music playing
playlists = {'brett': 'spotify:playlist:6VChS0ZQoRSOWTNsP7TgLZ', 'feel good':'spotify:playlist:5xGQTmhIGvBeaPCVUtKTZB'}
sp.start_playback(device_id=DEVICE_ID, context_uri=playlists['feel good'])
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

