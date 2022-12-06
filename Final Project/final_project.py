from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep
import re
import album_list
from adafruit_servokit import ServoKit

# Set channels to the number of servo channels on your kit.
# There are 16 channels on the PCA9685 chip.
kit = ServoKit(channels=16)

# Name and set up the servo according to the channel you are using.
servo = kit.continuous_servo[0]

# Set the pulse width range of your servo for PWM control of rotating 0-180 degree (min_pulse, max_pulse)
# Each servo might be different, you can normally find this information in the servo datasheet
servo.set_pulse_width_range(10, 0)

# spotify credentials
"""My credentials for spotify go here, for privacy reasons I removed them for github"""




reader=SimpleMFRC522()
sp.shuffle(False, device_id=DEVICE_ID)
prev = None
        
# infinite loop waiting for RFID scan
while True:
    try:
        id= reader.read()[0]
        status = album_list.get_album(id)
        sleep(.5)
        print(bool(status))
        if status:
            print(sp.album(status))
            sleep(0.25)
            sp.start_playback(device_id=DEVICE_ID, context_uri=status)
            sleep(.5)
            cur = sp.current_playback()
            artist = cur['item']['artists'][0]['name']
            artist = re.sub(r'[^\x00-\x7f]', "", artist)
            album = cur['item']['album']['name']
            print('Now playing: ' + album + ' by ' + artist) 
            sleep(.5)
            servo.throttle = 0
        else:
            servo.throttle = 1
            sleep(0.25)
            print('No album on this tag: ' + str(id))
        
    except KeyboardInterrupt:
        servo.throttle = 1
        sleep(0.5)
        break
