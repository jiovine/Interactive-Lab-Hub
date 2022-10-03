
import qwiic_i2c
import qwiic_button
import time
import sys

my_button1 = qwiic_button.QwiicButton()
my_button2 = qwiic_button.QwiicButton(0x5B)

def button_press():
    while True:
        if my_button1.is_button_pressed() == True:
            return 1
        if my_button2.is_button_pressed() == True:
            return 2

        time.sleep(0.1)
    