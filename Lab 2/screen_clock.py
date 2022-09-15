import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

from time import strftime, sleep
import datetime

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

#My images
image1 = Image.open("teams/dolphins.png")
image2 = Image.open("teams/ravens.png")

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", size=(162, height))
rotation = 90



# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
#font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
font = ImageFont.truetype("Freshman.ttf", 20)
time_font = ImageFont.truetype("Freshman.ttf", 25)

#Importing buttons
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()
                              

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

#Importing image of sun and rescaling
#image1 = image1.resize((int(image1.width//3.8), int(image1.height//3.8)), Image.BICUBIC)
image1 = image1.resize((int(height//2), int(width//4)), Image.BICUBIC)
image1 = image1.rotate(90, Image.NEAREST, expand = 1)

image2 = image2.resize((int(height//2), int(width//4)), Image.BICUBIC)
image2 = image2.rotate(90, Image.NEAREST, expand = 1)

nextGame = datetime.datetime(22, 9, 18, 13, 00, 00)


while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width-79, height-1), outline='white', fill=0)
    curDay=strftime("%d")
    curMonth=strftime("%m")
    curYear=strftime("%y")
    curHour=strftime("%H")
    curMinute=strftime("%M")
    curSecond=strftime("%S")
    
    now = datetime.datetime(int(curYear), int(curMonth), int(curDay), int(curHour), int(curMinute), int(curSecond))
    
    c = nextGame-now
    hours = int(c.total_seconds()//3600)
    minutes = int((c.total_seconds()%3600)//60)
    seconds = int((c.total_seconds()%3600)%60)
    if seconds < 10:
        seconds = '0'+str(seconds)
    if minutes < 10:
        minutes = '0'+str(minutes)
        
    delta = str(hours)+':'+str(minutes)+':'+str(seconds)
    

    
    #TODO: Lab 2 part D work should be filled in here. You should be able to look in cli_clock.py and stats.py
    x=0
    y=0
    title=['GAMEDAY', 'COUNTDOWN']
    disp.image(image1, x=5, y=5,)
    disp.image(image2, x=70, y=0)
    time = curHour+':'+curMinute+':'+curSecond
    draw.text((81-(font.getsize(title[0])[0]//2), 10), text=title[0], font=font, fill=(255,133,0,255))
    y += font.getsize('G')[1]
    draw.text((81-(font.getsize(title[1])[0]//2),y+15), text=title[1], font=font, fill=(255,133,0,255))
    y += font.getsize('C')[1]
    draw.text((81-(time_font.getsize(delta)[0]//2),y+45), text=delta, font=time_font, fill=(1,144,158,255))
    
    if not buttonA.value:
        draw.rectangle((0, 0, width-79, height-1), outline='white', fill=0)
        y=5
        inc=height//5
        draw.text((81-font.getsize('AFC EAST')[0]//2,y), text='AFC EAST', font=font, fill='white')
        y+=inc
        draw.text((5,y), text='Dolphins', font=font, fill=(1,144,158,255))
        draw.text((160-font.getsize('1-0')[0], y), text='1-0', font=font, fill='white')
        y+=inc
        draw.text((5,y), text='Bills', font=font, fill='blue')
        draw.text((160-font.getsize('1-0')[0], y), text='1-0', font=font, fill='white')
        y+=inc
        draw.text((5,y), text='Jets', font=font, fill='green')
        draw.text((160-font.getsize('1-0')[0], y), text='0-1', font=font, fill='white')
        y+=inc
        draw.text((5,y), text='Patriots', font=font, fill='red')
        draw.text((160-font.getsize('1-0')[0], y), text='0-1', font=font, fill='white')
    
    disp.image(image, rotation, y=78)
    
    
