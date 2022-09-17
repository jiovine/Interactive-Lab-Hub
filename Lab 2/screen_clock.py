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

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
partition = 80 # partitioning off the right side of the screen to fit the team logos
image = Image.new("RGB", size=(width-partition, height)) # resized to only display on left partition of screen
rotation = 90



# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
disp.image(image, rotation)


# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("Freshman.ttf", 20)
time_font = ImageFont.truetype("Freshman.ttf", 25)
win_font = ImageFont.truetype("Freshman.ttf", 30)
                              

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

# Importing the buttons
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Selecting the next game time
# Dictionary of game times (only 17) where key is team name and value is datetime value
game_times = {'patriots': 'W 20-3',
                'ravens': datetime.datetime(22, 9, 18, 13, 00, 00),
                'bills': datetime.datetime(22, 9, 25, 13, 00, 00),
                'bengals': datetime.datetime(22, 9, 29, 20, 15, 00),
                'jets': datetime.datetime(22, 10, 9, 13, 00, 00),
                'vikings': datetime.datetime(22, 10, 16, 13, 00, 00),
                'steelers': datetime.datetime(22, 10, 23, 20, 20, 00),
                'lions': datetime.datetime(22, 10, 30, 13, 00, 00),
                'bears': datetime.datetime(22, 11, 6, 13, 00, 00),
                'browns': datetime.datetime(22, 11, 13, 13, 00, 00),
                'texans': datetime.datetime(22, 11, 27, 13, 00, 00),
                '49ers': datetime.datetime(22, 12, 4, 16, 5, 00),
                'chargers': datetime.datetime(22, 12, 11, 16, 5, 00),
                'bills1': datetime.datetime(22, 12, 18, 13, 00, 00),
                'packers': datetime.datetime(22, 12, 25, 13, 00, 00),
                'patriots1': datetime.datetime(23, 1, 1, 13, 00, 00),
                'jets1': datetime.datetime(23, 1, 8, 13, 00, 00)
            }

# current count of the week the user wants to see, week 1 = 0th index
# starts the display on the correct next game instead of the beginning of the dictionary
count = 0
for v in game_times.values():
    if type(v) != str and datetime.datetime.today() > v: break
    count+=1

# assigning the proper team logo and next game time to display
team, next_game = list(game_times.items())[count]

while True:
    # Draw a black filled box to clear the image. (-1 so that the outline shows)
    draw.rectangle((0, 0, width-partition-1, height-1), outline='white', fill=0)

    # Selecting proper teams for the week, resizing to fit properly
    image1 = Image.open("teams/dolphins.png")
    image2 = Image.open("teams/{}.png".format(team))
    image1 = image1.resize((int(height//2), int(width//4)), Image.BICUBIC)
    image1 = image1.rotate(rotation, Image.NEAREST, expand = 1)
    image2 = image2.resize((int(height//2), int(width//4)), Image.BICUBIC)
    image2 = image2.rotate(rotation, Image.NEAREST, expand = 1)

    # Getting the current date and time
    curDay=strftime("%d")
    curMonth=strftime("%m")
    curYear=strftime("%y")
    curHour=strftime("%H")
    curMinute=strftime("%M")
    curSecond=strftime("%S")
    now = datetime.datetime(int(curYear), int(curMonth), int(curDay), int(curHour), int(curMinute), int(curSecond))
    

    # Displaying the gameday countdown and teams playing in their individual partitions
    if type(next_game) == str:
        disp.image(image1, x=5, y=5,)
        disp.image(image2, x=70, y=0)
        draw.text((81-(win_font.getsize(next_game)[0]//2), (height-win_font.getsize(next_game)[1])//2), text=next_game, font=win_font, fill=(255,133,0,255))


    else:
        c = next_game-now
        hours = int(c.total_seconds()//3600)
        minutes = int((c.total_seconds()%3600)//60)
        seconds = int((c.total_seconds()%3600)%60)
        if seconds < 10:
            seconds = '0'+str(seconds)
        if minutes < 10:
            minutes = '0'+str(minutes)
        delta = str(hours)+':'+str(minutes)+':'+str(seconds)
        x, y = 0, 0
        title=['GAMEDAY', 'COUNTDOWN']
        disp.image(image1, x=5, y=5,)
        disp.image(image2, x=70, y=0)
        time = curHour+':'+curMinute+':'+curSecond
        draw.text((81-(font.getsize(title[0])[0]//2), 10), text=title[0], font=font, fill=(255,133,0,255))
        y += font.getsize('G')[1]
        draw.text((81-(font.getsize(title[1])[0]//2),y+15), text=title[1], font=font, fill=(255,133,0,255))
        y += font.getsize('C')[1]
        draw.text((81-(time_font.getsize(delta)[0]//2),y+45), text=delta, font=time_font, fill=(1,144,158,255))


    # Displaying the divisional records for the teams
    if (not buttonA.value and not buttonB.value):
        draw.rectangle((0, 0, width-partition-1, height-1), outline='white', fill=0)
        y=5
        inc=height//5
        draw.text((partition-font.getsize('AFC EAST')[0]//2,y), text='AFC EAST', font=font, fill='white')
        y+=inc
        draw.text((5,y), text='Dolphins', font=font, fill=(1,144,158,255))
        draw.text(((width-partition-1)-font.getsize('1-0')[0], y), text='1-0', font=font, fill='white')
        y+=inc
        draw.text((5,y), text='Bills', font=font, fill='blue')
        draw.text(((width-partition-1)-font.getsize('1-0')[0], y), text='1-0', font=font, fill='white')
        y+=inc
        draw.text((5,y), text='Jets', font=font, fill='green')
        draw.text(((width-partition-1)-font.getsize('1-0')[0], y), text='0-1', font=font, fill='white')
        y+=inc
        draw.text((5,y), text='Patriots', font=font, fill='red')
        draw.text(((width-partition-1)-font.getsize('1-0')[0], y), text='0-1', font=font, fill='white')

    # advancing the count either forward or backward one week depending on which button is pressed
    elif not buttonA.value:
        if count < len(game_times.items())-1:
            count+=1
        else:
            count = (count+1)%len(game_times.keys())
        team, next_game = list(game_times.items())[count]

    elif not buttonB.value:
        if count > 0:
            count-=1
        else:
            count = (count-1)+len(game_times.keys())
        team, next_game = list(game_times.items())[count]

    
    disp.image(image, rotation, y=partition)