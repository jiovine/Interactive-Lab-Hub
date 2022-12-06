import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep

reader = SimpleMFRC522()

while True:
        try:
                print("Waiting for you to scan an RFID sticker/card")
                id = reader.read()[0]
                print("The ID for this card is:", id)
                
        finally:
                GPIO.cleanup()
        sleep(.5)